"""
GitHub 仓库 ZIP 下载工具（终端交互版）
运行后直接在终端输入 GitHub 链接，支持多个链接排队下载
下载文件命名规则：{owner}_{repo}@{short_sha}.zip
下载目录：程序所在目录

本次改动：
1) 下载全程写入 xxx.zip.part，校验通过才改名为最终文件。
2) 三层兜底清理 .part：
   - 失败/异常 → 立即删
   - 关闭窗口/注销/关机/atexit → 通过挂钩子尽力删
   - 下次启动扫描残留 → 无条件删
3) pip 风格进度条：进度行原地刷新，不再刷屏。
4) 底部两行动态区（进度行 + 输入行），输入内容不会被日志冲掉。
"""

import sys
import os
import time
import queue
import threading
import atexit
from urllib.parse import urlparse

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("❌ 缺少 requests 库，请执行：pip install requests")
    input("\n按回车键退出...")
    sys.exit(1)


IS_WINDOWS = (os.name == 'nt')
TMP_SUFFIX = '.zip.part'

# Windows 启用 ANSI 转义码支持
if IS_WINDOWS:
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass


# ============================================================
# 临时文件追踪器：记录所有正在写入的 .part 文件
# 事件钩子/atexit 触发时统一删除
# ============================================================
class PartialFileTracker:
    def __init__(self):
        self._files = set()
        self._lock = threading.Lock()

    def add(self, path):
        with self._lock:
            self._files.add(path)

    def discard(self, path):
        with self._lock:
            self._files.discard(path)

    def cleanup_all(self):
        with self._lock:
            paths = list(self._files)
            self._files.clear()
        for path in paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass


_tracker = PartialFileTracker()


def _install_exit_handlers():
    """安装各种退出时的清理钩子，尽量在进程消失前删掉 .part。"""
    atexit.register(_tracker.cleanup_all)

    if IS_WINDOWS:
        # Windows: 捕获窗口关闭(CTRL_CLOSE)、注销、关机事件
        try:
            import ctypes
            from ctypes import wintypes

            HANDLER = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)

            def _win_handler(ctrl_type):
                # 2=CTRL_CLOSE_EVENT, 5=LOGOFF, 6=SHUTDOWN
                if ctrl_type in (2, 5, 6):
                    _tracker.cleanup_all()
                return False  # 交回默认处理，让系统正常收尾

            # 必须保留引用，否则回调会被 GC 掉
            _install_exit_handlers._win_ref = HANDLER(_win_handler)
            ctypes.windll.kernel32.SetConsoleCtrlHandler(
                _install_exit_handlers._win_ref, True
            )
        except Exception:
            pass
    else:
        # Unix: SIGTERM / SIGHUP（SIGINT 保持 Python 默认 -> KeyboardInterrupt）
        import signal

        def _unix_handler(signum, frame):
            _tracker.cleanup_all()
            signal.signal(signum, signal.SIG_DFL)
            os.kill(os.getpid(), signum)

        for name in ('SIGTERM', 'SIGHUP'):
            sig = getattr(signal, name, None)
            if sig is not None:
                try:
                    signal.signal(sig, _unix_handler)
                except Exception:
                    pass


# ============================================================
# 终端交互：pip 风格进度条 + 固定输入行
# ============================================================
class ProgressConsole:
    """底部两行动态区：上行进度条，下行输入行。

    屏幕结构（\033[A 上移一行）：
        ...历史日志...
        [进度行]  ← progress_text，用 \r 原地刷新
        🔗 > xxx  ← 用户正在输入的内容，始终可见
    """

    def __init__(self, prompt):
        self.prompt = prompt
        self.buffer = ''
        self.lock = threading.RLock()
        self.progress_text = ''
        self.started = False
        self.closed = False

    def start(self):
        with self.lock:
            if self.started:
                return
            sys.stdout.write('\n' + self.prompt)
            sys.stdout.flush()
            self.started = True

    # -------- 读键 --------
    @staticmethod
    def _read_key():
        if IS_WINDOWS:
            import msvcrt
            while True:
                ch = msvcrt.getwch()
                if ch in ('\x00', '\xe0'):
                    msvcrt.getwch()
                    continue
                return ch

        import termios
        import tty
        try:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
        except Exception:
            return sys.stdin.read(1) or ''

        try:
            tty.setcbreak(fd)
            return sys.stdin.read(1)
        finally:
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except Exception:
                pass

    # -------- 读一行 --------
    def read_line(self):
        self.buffer = ''
        with self.lock:
            sys.stdout.write('\r' + self.prompt + '\033[K')
            sys.stdout.flush()

        while True:
            ch = self._read_key()

            if ch == '' or ch == '\x04':        # EOF / Ctrl+D
                with self.lock:
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    self.closed = True
                return None

            if ch == '\x03':                    # Ctrl+C
                raise KeyboardInterrupt

            if ch in ('\r', '\n'):
                line = self.buffer
                self._commit(line)
                return line

            if ch in ('\x7f', '\x08'):          # 退格
                with self.lock:
                    if self.buffer:
                        self.buffer = self.buffer[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                continue

            if ord(ch) < 32:
                continue

            with self.lock:
                self.buffer += ch
                sys.stdout.write(ch)
                sys.stdout.flush()

    def _commit(self, line):
        """回车：把输入行变成历史，重建进度行 + 新输入行。"""
        with self.lock:
            sys.stdout.write('\033[A\r\033[K')
            sys.stdout.write(self.prompt + line + '\n')
            sys.stdout.write('\r\033[K')
            sys.stdout.write(self.progress_text + '\n')
            sys.stdout.write(self.prompt)
            self.buffer = ''
            sys.stdout.flush()

    # -------- 进度行 --------
    def update_progress(self, text):
        if self.closed:
            return
        with self.lock:
            self.progress_text = text
            sys.stdout.write('\033[A\r' + text + '\033[K')
            sys.stdout.write('\033[B\r' + self.prompt + self.buffer + '\033[K')
            sys.stdout.flush()

    def clear_progress(self):
        if self.closed:
            return
        with self.lock:
            self.progress_text = ''
            sys.stdout.write('\033[A\r\033[K')
            sys.stdout.write('\033[B\r' + self.prompt + self.buffer + '\033[K')
            sys.stdout.flush()

    # -------- 日志 --------
    def log(self, message):
        if self.closed:
            return
        with self.lock:
            sys.stdout.write('\033[A\r\033[K')
            sys.stdout.write(message + '\n')
            sys.stdout.write('\r\033[K')
            sys.stdout.write(self.progress_text + '\n')
            sys.stdout.write(self.prompt + self.buffer + '\033[K')
            sys.stdout.flush()

    def finish(self, message=None):
        with self.lock:
            if self.closed:
                return
            self.closed = True
            sys.stdout.write('\033[A\r\033[K')
            if message:
                sys.stdout.write(message + '\n')
            sys.stdout.write('\r\033[K\n')
            sys.stdout.flush()


# ============================================================
# 主类
# ============================================================
class GitHubZipDownloader:
    PROMPT = "🔗 > "

    def __init__(self):
        self.script_dir = os.path.dirname(
            os.path.abspath(sys.argv[0] if sys.argv[0] else __file__)
        )

        self.max_retries = 999
        self.retry_delay = 10
        self.download_timeout = 60

        self.branch_cache = {}
        self.github_token = self._get_github_token()

        self.console = ProgressConsole(self.PROMPT)
        self.task_queue = queue.Queue()
        self.stop_event = threading.Event()

    # -------- 基础工具 --------
    def _get_github_token(self):
        token = os.environ.get('GITHUB_TOKEN', '')
        if token:
            return token
        token_file = os.path.join(self.script_dir, '.github_token')
        if os.path.exists(token_file):
            try:
                with open(token_file, 'r', encoding='utf-8') as f:
                    return f.read().strip() or None
            except Exception:
                pass
        return None

    def log(self, message):
        self.console.log(message)

    def progress(self, text):
        self.console.update_progress(text)

    @staticmethod
    def _safe_remove(path):
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

    def cleanup_partial_files(self):
        """启动时扫描并删除上次遗留的 .part 文件（最后一道兜底）"""
        removed = 0
        try:
            names = os.listdir(self.script_dir)
        except Exception:
            return
        for name in names:
            if not name.endswith(TMP_SUFFIX):
                continue
            try:
                os.remove(os.path.join(self.script_dir, name))
                removed += 1
            except Exception:
                pass
        if removed:
            print(f"🧹 已清理 {removed} 个上次遗留的未完成下载文件（*{TMP_SUFFIX}）")

    # -------- GitHub API --------
    def _get_api_headers(self):
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        return headers

    def extract_repo_info(self, url):
        try:
            url = url.strip().rstrip('/')
            if url.endswith('.git'):
                url = url[:-4]
            parsed = urlparse(url)
            if 'github.com' not in parsed.netloc:
                return None, None
            path = parsed.path.strip('/')
            parts = path.split('/')
            if len(parts) >= 2:
                return parts[0], parts[1].replace('.git', '')
            return None, None
        except Exception:
            return None, None

    def get_default_branch(self, owner, repo):
        cache_key = f"{owner}/{repo}"
        if cache_key in self.branch_cache:
            return self.branch_cache[cache_key]

        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        try:
            resp = requests.get(api_url, headers=self._get_api_headers(), timeout=15)
            if resp.status_code == 200:
                branch = resp.json().get('default_branch')
                if branch:
                    self.branch_cache[cache_key] = branch
                    return branch
            elif resp.status_code == 403 and 'X-RateLimit-Remaining' in resp.headers:
                reset_time = int(resp.headers.get('X-RateLimit-Reset', 0))
                wait = max(reset_time - int(time.time()), 0) + 5
                self.log(f"⚠️ GitHub API 速率限制，等待 {wait} 秒")
                time.sleep(wait)
                return self.get_default_branch(owner, repo)
        except Exception as e:
            self.log(f"⚠️ API 获取分支失败: {e}")

        for candidate in ('main', 'master'):
            test_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{candidate}.zip"
            try:
                resp = requests.head(test_url, allow_redirects=True, timeout=10)
                if resp.status_code == 200:
                    self.branch_cache[cache_key] = candidate
                    return candidate
            except Exception:
                continue

        self.branch_cache[cache_key] = None
        return None

    def get_latest_commit_sha(self, owner, repo, branch):
        api_url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
        try:
            resp = requests.get(api_url, headers=self._get_api_headers(), timeout=15)
            if resp.status_code == 200:
                sha = resp.json().get('commit', {}).get('sha')
                if sha:
                    return sha
            elif resp.status_code == 403:
                reset_time = int(resp.headers.get('X-RateLimit-Reset', 0))
                wait = max(reset_time - int(time.time()), 0) + 5
                self.log(f"⚠️ GitHub API 速率限制，等待 {wait} 秒")
                time.sleep(wait)
                return self.get_latest_commit_sha(owner, repo, branch)
            else:
                self.log(f"⚠️ 获取 commit SHA 失败 HTTP {resp.status_code}: {owner}/{repo}")
        except Exception as e:
            self.log(f"⚠️ 获取 commit SHA 异常: {e}")
        return None

    @staticmethod
    def get_zip_url(owner, repo, branch):
        return f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"

    # -------- 下载 --------
    @staticmethod
    def _render_bar(pct, width=24):
        filled = int(pct / 100.0 * width)
        filled = max(0, min(filled, width))
        return '█' * filled + '░' * (width - filled)

    def download_zip(self, url, dest_path, label):
        tmp_path = dest_path + TMP_SUFFIX
        _tracker.add(tmp_path)
        downloaded = 0
        start = time.time()

        try:
            self._safe_remove(tmp_path)

            response = requests.get(
                url,
                stream=True,
                timeout=(10, self.download_timeout),
                headers={'Accept-Encoding': 'identity'},
            )
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            content_encoding = (response.headers.get('content-encoding') or '').lower()
            size_known = total_size > 0 and content_encoding in ('', 'identity')

            last_report = 0.0
            with open(tmp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=65536):
                    if not chunk:
                        continue
                    f.write(chunk)
                    downloaded += len(chunk)

                    now = time.time()
                    if now - last_report >= 0.2:
                        elapsed = max(now - start, 0.001)
                        speed = downloaded / 1048576 / elapsed
                        if size_known:
                            pct = downloaded * 100.0 / total_size
                            bar = self._render_bar(pct)
                            self.progress(
                                f"   ⬇️  {label[:32]} [{bar}] "
                                f"{pct:5.1f}%  "
                                f"{downloaded / 1048576:6.1f}/{total_size / 1048576:.1f}MB  "
                                f"{speed:5.2f}MB/s"
                            )
                        else:
                            self.progress(
                                f"   ⬇️  {label[:32]}  "
                                f"{downloaded / 1048576:6.1f}MB  "
                                f"{speed:5.2f}MB/s"
                            )
                        last_report = now

                f.flush()
                os.fsync(f.fileno())

            actual_size = os.path.getsize(tmp_path)
            if size_known and actual_size != total_size:
                raise Exception(f"下载不完整：{actual_size} / {total_size} 字节")

            # 校验通过：改名为正式文件，同时从追踪器摘除
            os.replace(tmp_path, dest_path)
            _tracker.discard(tmp_path)

            elapsed = max(time.time() - start, 0.001)
            self.console.clear_progress()
            self.log(f"   ⬆️  传输完成 {downloaded / 1048576:.1f}MB / {elapsed:.1f}s "
                     f"({downloaded / 1048576 / elapsed:.2f} MB/s)")
            return True, None

        except KeyboardInterrupt:
            _tracker.discard(tmp_path)
            self._safe_remove(tmp_path)
            raise
        except Exception as e:
            _tracker.discard(tmp_path)
            self._safe_remove(tmp_path)
            return False, str(e)

    @staticmethod
    def should_retry_error(error_msg):
        if not error_msg:
            return False
        keywords = ('timeout', 'timed out', 'connection', 'network', 'unreachable',
                    'refused', 'reset', 'broken pipe', 'eof', 'rate limit', 'ssl',
                    '不完整')
        return any(k in error_msg.lower() for k in keywords)

    # -------- 单任务 --------
    def process_url(self, url):
        owner, repo = self.extract_repo_info(url)
        if not owner or not repo:
            self.log(f"❌ 无效的 GitHub 链接: {url}")
            return False

        self.log(f"📦 正在处理: {owner}/{repo}")

        branch = self.get_default_branch(owner, repo)
        if not branch:
            self.log(f"❌ 无法获取默认分支: {url}")
            return False

        latest_sha = self.get_latest_commit_sha(owner, repo, branch)
        if not latest_sha:
            self.log(f"❌ 无法获取最新 commit SHA: {url}")
            return False

        short_sha = latest_sha[:7]
        zip_name = f"{owner}_{repo}@{short_sha}.zip"
        zip_path = os.path.join(self.script_dir, zip_name)

        if os.path.exists(zip_path):
            self.log(f"✅ 文件已存在，跳过: {zip_name}")
            return True

        zip_url = self.get_zip_url(owner, repo, branch)

        last_error = None
        for attempt in range(self.max_retries + 1):
            if attempt > 0:
                self.log(f"🔄 重试 #{attempt}/{self.max_retries}: {owner}/{repo}")
                time.sleep(self.retry_delay)

            success, err = self.download_zip(zip_url, zip_path, zip_name)
            if success:
                self.log(f"✅ 下载完成: {zip_name}")
                return True

            last_error = err
            if not self.should_retry_error(err):
                self.log(f"❌ 下载失败（不可重试）: {err}")
                break

        self.log(f"❌ 下载失败: {url} ({last_error})")
        return False

    # -------- 工作线程 --------
    def _worker_loop(self):
        while not self.stop_event.is_set():
            try:
                url = self.task_queue.get(timeout=0.5)
            except queue.Empty:
                continue
            try:
                self.process_url(url)
            except Exception as e:
                self.log(f"💥 处理出错: {url} - {e}")
            finally:
                self.task_queue.task_done()

    # -------- 主流程 --------
    def print_banner(self):
        print("=" * 60)
        print("🚀 GitHub ZIP 下载工具（终端交互版）")
        print("=" * 60)
        print(f"📁 下载目录: {self.script_dir}")
        print("💡 输入 GitHub 仓库链接后回车即可加入下载队列")
        print("💡 支持一次粘贴多个链接（空格/换行分隔）")
        print("💡 输入 exit / quit / q 退出程序")
        print(f"💡 下载中的文件为 *{TMP_SUFFIX}，完成后才改名为正式 zip")
        print("=" * 60)

    def run(self):
        self.print_banner()
        self.cleanup_partial_files()          # 第三层兜底：启动扫描
        self.stop_event.clear()

        self.console.start()

        worker = threading.Thread(target=self._worker_loop, daemon=True)
        worker.start()

        try:
            while True:
                line = self.console.read_line()
                if line is None:
                    break

                line = line.strip()
                if not line:
                    continue
                if line.lower() in ('exit', 'quit', 'q'):
                    break

                tokens = line.split()
                if not tokens:
                    continue
                for token in tokens:
                    self.task_queue.put(token)
                self.log(f"📥 已加入 {len(tokens)} 个链接到队列 "
                         f"(待处理: {self.task_queue.qsize()})")
        except KeyboardInterrupt:
            pass
        finally:
            self._shutdown()

    def _shutdown(self):
        if self.task_queue.unfinished_tasks > 0:
            self.log(f"⏳ 队列中还有 {self.task_queue.unfinished_tasks} 个任务，"
                     f"等待完成...（按 Ctrl+C 强制退出）")
            try:
                self.task_queue.join()
            except KeyboardInterrupt:
                self.console.finish("🛑 强制退出")
                _tracker.cleanup_all()
                os._exit(1)

        self.stop_event.set()
        self.console.finish("👋 程序退出")


def main():
    _install_exit_handlers()
    try:
        downloader = GitHubZipDownloader()
        downloader.run()
    except KeyboardInterrupt:
        print("\n🛑 程序被用户中断")
    except Exception as e:
        print(f"💥 程序发生严重错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()