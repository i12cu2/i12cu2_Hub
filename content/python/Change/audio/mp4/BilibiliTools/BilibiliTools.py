import os
import re
import sys
import json
import hashlib
import shutil
import subprocess
import time
import random
import threading
import urllib.parse
import requests
from functools import reduce
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed


# ==================== 配置 ====================
# 可选：填 cookies.txt 的路径（用 "Get cookies.txt LOCALLY" 扩展导出）
COOKIES_FILE = ""
# 可选：从哪个浏览器读 cookie（chrome / edge / firefox）
# 建议留空走 cookies.txt；如果要用浏览器直读，填 'firefox' 最稳
COOKIES_FROM_BROWSER = "firefox"


# ==================== 程序目录 ====================
def get_program_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


PROGRAM_DIR = get_program_dir()
SAVE_PATH = PROGRAM_DIR


# ==================== 外部工具查找 ====================
def find_ffmpeg():
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if ffmpeg and ffprobe:
        return ffmpeg, ffprobe
    common_paths = [
        r"C:\Program File\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
        r"C:\ffmpeg\bin",
        os.path.join(os.environ.get("USERPROFILE", ""), "ffmpeg", "bin"),
    ]
    for base in common_paths:
        exe = os.path.join(base, "ffmpeg.exe")
        probe = os.path.join(base, "ffprobe.exe")
        if os.path.isfile(exe) and os.path.isfile(probe):
            return exe, probe
    return None, None


def find_ytdlp():
    path = shutil.which("yt-dlp")
    if path:
        return path
    candidates = [
        os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Programs", "Python"),
        r"C:\Python312\Scripts",
        r"C:\Python311\Scripts",
        r"C:\Python310\Scripts",
    ]
    for base in candidates:
        for name in ("yt-dlp.exe", "yt-dlp"):
            exe = os.path.join(base, name)
            if os.path.isfile(exe):
                return exe
    return None


FFMPEG_PATH, FFPROBE_PATH = find_ffmpeg()
YTDLP_PATH = find_ytdlp()


# ==================== WBI 签名器（备用） ====================
class WbiSigner:
    MIXIN_KEY_ENC_TAB = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
        27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
        37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
        22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52
    ]

    def __init__(self, session):
        self.session = session
        self.mixin_key = None

    def _get_mixin_key(self, orig):
        return reduce(lambda s, i: s + orig[i], self.MIXIN_KEY_ENC_TAB, '')[:32]

    def _fetch_keys(self):
        try:
            resp = self.session.get(
                "https://api.bilibili.com/x/web-interface/nav", timeout=10)
            data = resp.json()
            wbi_img = data.get('data', {}).get('wbi_img')
            if not wbi_img:
                return False
            img_key = wbi_img.get('img_url', '').rsplit('/', 1)[-1].split('.')[0]
            sub_key = wbi_img.get('sub_url', '').rsplit('/', 1)[-1].split('.')[0]
            self.mixin_key = self._get_mixin_key(img_key + sub_key)
            return True
        except Exception:
            return False

    def sign(self, params):
        if not self.mixin_key:
            self._fetch_keys()
        if not self.mixin_key:
            return params
        params = dict(params)
        params['wts'] = int(time.time())
        params = dict(sorted(params.items()))
        query = urllib.parse.urlencode(params)
        params['w_rid'] = hashlib.md5((query + self.mixin_key).encode()).hexdigest()
        return params


# ==================== 主类 ====================
class BilibiliTool:
    MODES = {'mp3', 'cover', 'intro', 'all'}
    MAX_WORKERS = 3

    def __init__(self, save_path=SAVE_PATH):
        self.save_path = save_path
        self.session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com/',
            'Origin': 'https://www.bilibili.com',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.session.headers.update(headers)

        self.ffmpeg_path = FFMPEG_PATH
        self.ffmpeg_ok = bool(self.ffmpeg_path and os.path.exists(self.ffmpeg_path))
        self.ytdlp_path = YTDLP_PATH
        self.ytdlp_ok = bool(self.ytdlp_path)

        self._print_lock = threading.Lock()
        self.wbi = WbiSigner(self.session)
        os.makedirs(save_path, exist_ok=True)

    # ==================== 基础工具 ====================
    def _sanitize(self, name, max_len=80):
        if not name:
            return "未命名"
        name = re.sub(r'<[^>]+>', '', name)
        for ch in '<>:"/\\|?*':
            name = name.replace(ch, '_')
        name = name.strip().strip('.')
        if not name:
            name = "未命名"
        if len(name) > max_len:
            name = name[:max_len]
        return name

    def _is_uploader_url(self, s):
        return bool(re.search(r'space\.bilibili\.com/(\d+)', s))

    def _extract_mid(self, s):
        m = re.search(r'space\.bilibili\.com/(\d+)', s)
        return m.group(1) if m else None

    def _extract_bvid(self, s):
        if re.match(r'^BV[0-9A-Za-z]{10}$', s):
            return s
        m = re.search(r'BV[0-9A-Za-z]{10}', s)
        return m.group() if m else None

    def _safe_print(self, msg):
        with self._print_lock:
            print(msg)

    def _request(self, url, params=None, timeout=15):
        time.sleep(random.uniform(0.2, 0.5))
        r = self.session.get(url, params=params, timeout=timeout)
        text = r.text
        if text.lstrip().startswith('<'):
            raise RuntimeError("B站返回了 HTML 而不是 JSON，可能被风控。")
        return r

    # ==================== 视频信息 ====================
    def _get_video_info(self, bvid):
        url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        r = self._request(url)
        data = r.json()
        if data['code'] != 0:
            raise Exception(f"获取视频信息失败: {data.get('message', '未知错误')}")
        d = data['data']
        return {
            'title': self._sanitize(d.get('title', ''), 60),
            'raw_title': d.get('title', ''),
            'bvid': bvid,
            'pic': d.get('pic', ''),
            'pages': d.get('pages') or [{
                'cid': d.get('cid'),
                'page': 1,
                'part': d.get('title', ''),
            }],
            'desc': d.get('desc', ''),
            'pubdate': d.get('pubdate', 0),
            'ugc_season': d.get('ugc_season'),
        }

    def _get_play_url(self, bvid, cid):
        url = (f"https://api.bilibili.com/x/player/playurl"
               f"?bvid={bvid}&cid={cid}&qn=80&type=&otype=json")
        r = self._request(url)
        data = r.json()
        if data['code'] != 0:
            raise Exception(f"获取播放链接失败: {data.get('message', '未知错误')}")
        return data['data']['durl'][0]['url']

    # ==================== UP主信息 ====================
    def _get_uploader_info(self, mid):
        try:
            url = f"https://api.bilibili.com/x/web-interface/card?mid={mid}"
            r = self._request(url, timeout=10)
            data = r.json()
            if data['code'] == 0:
                return {'name': data['data']['card']['name'], 'mid': mid}
        except Exception as e:
            print(f"获取 UP 主信息失败: {e}")
        return None

    def _get_uploader_videos_via_ytdlp(self, mid):
        """用 yt-dlp 获取 UP 主视频列表，逐行打印 id + title"""
        if not self.ytdlp_ok:
            print("  未找到 yt-dlp。")
            return None

        url = f"https://space.bilibili.com/{mid}/video"
        # 让 yt-dlp 每行输出 id<TAB>title，简单又稳定
        cmd = [
            self.ytdlp_path,
            '--flat-playlist',
            '--no-warnings',
            '--ignore-config',
            '--print', '%(id)s\t%(title)s',
        ]
        # cookie 参数
        if COOKIES_FILE and os.path.isfile(COOKIES_FILE):
            cmd.extend(['--cookies', COOKIES_FILE])
        elif COOKIES_FROM_BROWSER:
            cmd.extend(['--cookies-from-browser', COOKIES_FROM_BROWSER])
        cmd.append(url)

        print(f"  调用 yt-dlp: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=300
            )
            # 把 stderr 的前几行打出来，方便看到 yt-dlp 的实际输出
            if result.stderr:
                err_lines = result.stderr.strip().splitlines()
                if err_lines:
                    print("  yt-dlp 输出：")
                    for line in err_lines[-5:]:
                        print(f"    {line}")

            if result.returncode != 0:
                print(f"  yt-dlp 返回非零退出码 {result.returncode}")
                return None

            if not result.stdout.strip():
                print("  yt-dlp 没有返回任何内容。")
                return []

            videos = []
            for line in result.stdout.strip().splitlines():
                line = line.strip()
                if not line:
                    continue
                if '\t' in line:
                    vid, title = line.split('\t', 1)
                else:
                    vid, title = line, line
                vid = vid.strip()
                title = title.strip()
                if not vid:
                    continue
                if not vid.startswith('BV'):
                    continue
                videos.append({
                    'title': self._sanitize(title, 60),
                    'raw_title': title,
                    'bvid': vid,
                })

            print(f"  yt-dlp 解析到 {len(videos)} 个视频")
            return videos

        except subprocess.TimeoutExpired:
            print("  yt-dlp 获取列表超时。")
            return None
        except Exception as e:
            print(f"  yt-dlp 调用失败: {e}")
            return None

    def _get_uploader_videos_via_wbi(self, mid, max_pages=200):
        """备用：WBI 签名方式"""
        all_videos = []
        page_num = 1
        page_size = 30
        total = None

        if not self.wbi.mixin_key:
            self.wbi._fetch_keys()

        while page_num <= max_pages:
            try:
                url = "https://api.bilibili.com/x/space/wbi/arc/search"
                raw_params = {
                    'mid': mid,
                    'ps': page_size,
                    'pn': page_num,
                    'order': 'pubdate',
                    'platform': 'web',
                    'web_location': 1550101,
                }
                params = self.wbi.sign(raw_params)
                r = self._request(url, params=params)
                data = r.json()

                if data['code'] != 0:
                    msg = data.get('message', '未知错误')
                    if data['code'] in (-352, -412, -799):
                        print(f"  遇到频率限制，等待 5 秒后重试...")
                        time.sleep(5)
                        continue
                    print(f"  获取视频列表失败 (code={data['code']}): {msg}")
                    break

                vlist = data['data']['list']['vlist']
                if not vlist:
                    break

                if total is None:
                    total = data['data']['page']['count']
                    print(f"  UP 主共有 {total} 个视频，正在获取列表...")

                for item in vlist:
                    all_videos.append({
                        'title': self._sanitize(item.get('title', ''), 60),
                        'raw_title': item.get('title', ''),
                        'bvid': item.get('bvid', ''),
                    })

                print(f"  已获取 {len(all_videos)}/{total} 个视频")

                page_info = data['data']['page']
                if page_info['pn'] * page_info['ps'] >= page_info['count']:
                    break

                page_num += 1
                time.sleep(random.uniform(1.2, 2.5))

            except Exception as e:
                print(f"  获取第 {page_num} 页失败: {e}")
                break

        return all_videos

    def _get_uploader_videos(self, mid):
        videos = self._get_uploader_videos_via_ytdlp(mid)
        if videos is not None:
            return videos
        print("  yt-dlp 失败，改用内置方式重试...")
        return self._get_uploader_videos_via_wbi(mid)

    # ==================== 文件下载 ====================
    def _download_file(self, url, final_path, extra_headers=None):
        if os.path.exists(final_path):
            return 'exists'
        part_path = final_path + '.part'
        headers = {
            'User-Agent': self.session.headers['User-Agent'],
            'Referer': 'https://www.bilibili.com/'
        }
        if extra_headers:
            headers.update(extra_headers)

        try:
            r = self.session.get(url, headers=headers, stream=True, timeout=30)
            r.raise_for_status()
            with open(part_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
            if os.path.getsize(part_path) < 512:
                os.remove(part_path)
                return False
            if os.path.exists(final_path):
                os.remove(final_path)
            os.replace(part_path, final_path)
            return True
        except Exception:
            if os.path.exists(part_path):
                try:
                    os.remove(part_path)
                except Exception:
                    pass
            return False

    def _download_video(self, video_url, base_name, save_dir):
        final_path = os.path.join(save_dir, base_name + '.mp4')
        if os.path.exists(final_path):
            return final_path
        for attempt in range(2):
            ok = self._download_file(video_url, final_path)
            if ok == 'exists' or ok is True:
                return final_path
            if attempt == 0:
                time.sleep(1)
        return None

    def _convert_mp4_to_mp3(self, mp4_path):
        if not self.ffmpeg_ok:
            print("缺少 ffmpeg，无法转换 MP3。")
            return None
        if not os.path.exists(mp4_path):
            print(f"找不到视频文件: {mp4_path}")
            return None

        mp3_path = os.path.splitext(mp4_path)[0] + '.mp3'
        if os.path.exists(mp3_path):
            return mp3_path

        part_path = mp3_path + '.part'
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', mp4_path,
                '-vn', '-acodec', 'libmp3lame',
                '-q:a', '0',
                '-f', 'mp3',
                '-y', part_path
            ]
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600
            )
            if result.returncode == 0 and os.path.exists(part_path) and os.path.getsize(part_path) > 512:
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
                os.replace(part_path, mp3_path)
                return mp3_path
            else:
                err = result.stderr.decode('utf-8', errors='ignore') if isinstance(result.stderr, bytes) else str(result.stderr)
                print(f"  ffmpeg 转换失败（返回码 {result.returncode}）")
                if err:
                    for line in err.strip().splitlines()[-5:]:
                        print(f"    {line}")
                if os.path.exists(part_path):
                    try:
                        os.remove(part_path)
                    except Exception:
                        pass
                return None
        except subprocess.TimeoutExpired:
            print("  转换超时")
            if os.path.exists(part_path):
                try:
                    os.remove(part_path)
                except Exception:
                    pass
            return None
        except Exception as e:
            print(f"  转换出错: {e}")
            if os.path.exists(part_path):
                try:
                    os.remove(part_path)
                except Exception:
                    pass
            return None

    def _download_cover(self, pic_url, base_name, save_dir):
        if not pic_url:
            return None
        ext = os.path.splitext(urlparse(pic_url).path)[1] or '.jpg'
        final_path = os.path.join(save_dir, base_name + '_封面' + ext)
        ok = self._download_file(pic_url, final_path)
        if ok in (True, 'exists'):
            return final_path
        return None

    # ==================== 简介写入 ====================
    def _write_single_desc(self, filepath, desc_info):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"标题: {desc_info['title']}\n")
            f.write(f"BV号: {desc_info['bvid']}\n")
            pub = time.strftime('%Y-%m-%d', time.localtime(desc_info.get('pubdate', 0))) if desc_info.get('pubdate') else '未知'
            f.write(f"发布时间: {pub}\n")
            f.write(f"简介:\n{desc_info.get('desc', '')}\n")
        return filepath

    def _write_multi_desc(self, filepath, header, desc_list):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{header}\n")
            f.write(f"视频数量: {len(desc_list)}\n")
            f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            for i, v in enumerate(desc_list, 1):
                f.write(f"【视频 {i}】\n")
                f.write(f"标题: {v['title']}\n")
                f.write(f"BV号: {v['bvid']}\n")
                pub = time.strftime('%Y-%m-%d', time.localtime(v.get('pubdate', 0))) if v.get('pubdate') else '未知'
                f.write(f"发布时间: {pub}\n")
                f.write(f"简介:\n{v.get('desc', '')}\n")
                f.write("-" * 70 + "\n\n")
        return filepath

    # ==================== 单个任务处理 ====================
    def _process_one(self, task):
        bvid = task['bvid']
        cid = task['cid']
        base_name = task['base_name']
        save_dir = task['save_dir']
        mode = task['mode']

        try:
            if mode == 'cover':
                cover = self._download_cover(task.get('pic_url'), base_name, save_dir)
                return (cover, None)

            mp4_path = os.path.join(save_dir, base_name + '.mp4')
            mp3_path = os.path.join(save_dir, base_name + '.mp3')

            if mode == 'mp3':
                if os.path.exists(mp3_path):
                    return (None, mp3_path)
                if os.path.exists(mp4_path):
                    result = self._convert_mp4_to_mp3(mp4_path)
                    if result:
                        try:
                            os.remove(mp4_path)
                        except Exception:
                            pass
                        return (None, result)
                    return (mp4_path, None)

                video_url = self._get_play_url(bvid, cid)
                video_path = self._download_video(video_url, base_name, save_dir)
                if not video_path:
                    return (None, None)
                result = self._convert_mp4_to_mp3(video_path)
                if result:
                    try:
                        os.remove(video_path)
                    except Exception:
                        pass
                    return (None, result)
                return (video_path, None)

            if os.path.exists(mp4_path):
                video_path = mp4_path
            else:
                video_url = self._get_play_url(bvid, cid)
                video_path = self._download_video(video_url, base_name, save_dir)
                if not video_path:
                    return (None, None)

            if mode == 'all':
                self._download_cover(task.get('pic_url'), base_name, save_dir)
                if task.get('desc_info'):
                    desc_path = os.path.join(save_dir, base_name + '_简介.txt')
                    self._write_single_desc(desc_path, task['desc_info'])

            return (video_path, None)

        except Exception as e:
            self._safe_print(f"  处理出错: {e}")
            return (None, None)

    # ==================== 异步执行 ====================
    def _async_run(self, tasks, total):
        results = [None] * len(tasks)
        completed = [0]
        lock = threading.Lock()

        def worker(i, task):
            r = self._process_one(task)
            with lock:
                completed[0] += 1
                name = task.get('base_name', '')[:40]
                sys.stdout.write(f"\r已完成 {completed[0]}/{total}  {name:<45}")
                sys.stdout.flush()
            return r

        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as ex:
            futures = {ex.submit(worker, i, t): i for i, t in enumerate(tasks)}
            for f in as_completed(futures):
                i = futures[f]
                try:
                    results[i] = f.result()
                except Exception as e:
                    with lock:
                        print(f"\n  任务出错: {e}")
                    results[i] = (None, None)

        print()
        return results

    # ==================== 视频 URL 处理 ====================
    def _handle_video_url(self, input_str, mode):
        bvid = self._extract_bvid(input_str)
        if not bvid:
            raise ValueError("没有找到视频编号（BV号）")

        print(f"找到视频编号: {bvid}")
        print("正在获取视频信息...")
        info = self._get_video_info(bvid)
        title = info['title']
        pages = info['pages']
        total_pages = len(pages)

        print(f"视频标题: {info['raw_title']}")

        if total_pages == 1 and mode == 'cover':
            save_dir = self.save_path
        else:
            folder_name = self._sanitize(title, 60)
            save_dir = os.path.join(self.save_path, folder_name)
            os.makedirs(save_dir, exist_ok=True)
            if total_pages > 1:
                print(f"这是一个合集，共 {total_pages} 个视频。")
            print(f"保存到: {save_dir}")

        if total_pages == 1:
            page = pages[0]
            task = {
                'bvid': bvid, 'cid': page['cid'],
                'base_name': title, 'save_dir': save_dir,
                'mode': mode, 'pic_url': info['pic'],
                'desc_info': {
                    'title': info['raw_title'],
                    'bvid': bvid,
                    'pubdate': info['pubdate'],
                    'desc': info['desc'],
                },
            }
            result = self._process_one(task)
            print(self._result_summary(mode, result))
            return [result]

        tasks = []
        for idx, page in enumerate(pages, 1):
            page_num = page.get('page', idx)
            part_title = page.get('part') or f"P{page_num}"
            base = f"P{page_num}_" + self._sanitize(part_title, 80)
            tasks.append({
                'bvid': bvid, 'cid': page['cid'],
                'base_name': base, 'save_dir': save_dir,
                'mode': mode, 'pic_url': info['pic'],
                'desc_info': {
                    'title': info['raw_title'],
                    'bvid': bvid,
                    'pubdate': info['pubdate'],
                    'desc': info['desc'],
                },
            })

        print()
        return self._async_run(tasks, total_pages)

    # ==================== UP主处理 ====================
    def _handle_uploader(self, input_str, mode):
        mid = self._extract_mid(input_str)
        if not mid:
            raise ValueError("无法从链接中提取 UP 主 ID")

        print(f"识别到 UP 主主页，ID: {mid}")
        print("正在获取 UP 主信息...")
        up_info = self._get_uploader_info(mid)
        up_name = self._sanitize(up_info['name'] if up_info else f"UP_{mid}", 60)
        print(f"UP 主名字: {up_name}")

        print("正在获取 UP 主的视频列表...")
        videos = self._get_uploader_videos(mid)
        if not videos:
            print("没有找到任何视频。")
            if not self.ytdlp_ok:
                print("  提示：未检测到 yt-dlp，建议安装：pip install yt-dlp")
            return

        total = len(videos)
        print(f"\n共找到 {total} 个视频。")
        print("视频列表（前 10 个）：")
        for i, v in enumerate(videos[:10], 1):
            print(f"  {i}. {v['raw_title']}")
        if total > 10:
            print(f"  ... 还有 {total - 10} 个")

        up_dir = os.path.join(self.save_path, up_name)
        os.makedirs(up_dir, exist_ok=True)
        print(f"\n保存到: {up_dir}")

        if mode == 'intro':
            print(f"\n正在逐个获取 {total} 个视频的简介...")
            desc_list = []
            for i, v in enumerate(videos, 1):
                print(f"  [{i}/{total}] {v['raw_title']}")
                try:
                    info = self._get_video_info(v['bvid'])
                    desc_list.append({
                        'title': info['raw_title'],
                        'bvid': v['bvid'],
                        'pubdate': info['pubdate'],
                        'desc': info['desc'],
                    })
                except Exception as e:
                    print(f"    失败: {e}")
                time.sleep(random.uniform(0.4, 1.0))
            filepath = os.path.join(up_dir, f"{up_name}_简介.txt")
            self._write_multi_desc(filepath, f"UP主: {up_name} (mid: {mid})", desc_list)
            print(f"\n简介已保存到: {filepath}")
            return

        tasks = []
        if mode == 'all':
            for v in videos:
                try:
                    info = self._get_video_info(v['bvid'])
                    folder_name = self._sanitize(v['title'], 60)
                    sub_dir = os.path.join(up_dir, folder_name)
                    os.makedirs(sub_dir, exist_ok=True)
                    for page in info['pages']:
                        page_num = page.get('page', 1)
                        part_title = page.get('part') or v['raw_title']
                        if len(info['pages']) > 1:
                            base = self._sanitize(f"{folder_name}_P{page_num}_{part_title}", 80)
                        else:
                            base = folder_name
                        tasks.append({
                            'bvid': v['bvid'], 'cid': page['cid'],
                            'base_name': base, 'save_dir': sub_dir,
                            'mode': 'all', 'pic_url': info['pic'],
                            'desc_info': {
                                'title': info['raw_title'],
                                'bvid': v['bvid'],
                                'pubdate': info['pubdate'],
                                'desc': info['desc'],
                            },
                        })
                except Exception as e:
                    print(f"  获取 {v['raw_title']} 信息失败: {e}")
        else:
            for v in videos:
                try:
                    info = self._get_video_info(v['bvid'])
                    for page in info['pages']:
                        page_num = page.get('page', 1)
                        part_title = page.get('part') or v['raw_title']
                        if len(info['pages']) > 1:
                            base = self._sanitize(f"{v['title']}_P{page_num}_{part_title}", 80)
                        else:
                            base = self._sanitize(v['title'], 80)
                        tasks.append({
                            'bvid': v['bvid'], 'cid': page['cid'],
                            'base_name': base, 'save_dir': up_dir,
                            'mode': mode, 'pic_url': info['pic'],
                        })
                except Exception as e:
                    print(f"  获取 {v['raw_title']} 信息失败: {e}")

        if not tasks:
            print("没有可下载的视频。")
            return

        print(f"\n共 {len(tasks)} 个下载任务，开始下载...")
        return self._async_run(tasks, len(tasks))

    # ==================== 简介模式 ====================
    def _handle_intro(self, input_str):
        if self._is_uploader_url(input_str):
            return self._handle_uploader(input_str, 'intro')

        bvid = self._extract_bvid(input_str)
        if not bvid:
            raise ValueError("没有找到视频编号（BV号）")

        print(f"找到视频编号: {bvid}")
        print("正在获取视频信息...")
        info = self._get_video_info(bvid)

        season = info.get('ugc_season')
        if season:
            season_title = self._sanitize(season.get('title', '视频合集'), 60)
            episodes = []
            seen = set()
            for sec in season.get('sections', []):
                for ep in sec.get('episodes', []):
                    ep_bvid = ep.get('bvid')
                    if ep_bvid and ep_bvid not in seen:
                        seen.add(ep_bvid)
                        episodes.append({'bvid': ep_bvid, 'title': ep.get('title', '')})

            print(f"这是一个视频合集: {season_title}")
            print(f"共 {len(episodes)} 个视频，正在获取简介...")

            desc_list = []
            for i, ep in enumerate(episodes, 1):
                print(f"  [{i}/{len(episodes)}] {ep['title']}")
                try:
                    ep_info = self._get_video_info(ep['bvid'])
                    desc_list.append({
                        'title': ep_info['raw_title'],
                        'bvid': ep['bvid'],
                        'pubdate': ep_info['pubdate'],
                        'desc': ep_info['desc'],
                    })
                except Exception as e:
                    print(f"    失败: {e}")
                time.sleep(random.uniform(0.4, 1.0))

            folder = os.path.join(self.save_path, season_title)
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, f"{season_title}_简介.txt")
            self._write_multi_desc(filepath, f"合集标题: {season_title}", desc_list)
            print(f"\n简介已保存到: {filepath}")
            return filepath

        filepath = os.path.join(self.save_path, f"{info['title']}_简介.txt")
        self._write_single_desc(filepath, {
            'title': info['raw_title'],
            'bvid': bvid,
            'pubdate': info['pubdate'],
            'desc': info['desc'],
        })
        print(f"\n简介已保存到: {filepath}")
        return filepath

    # ==================== 结果摘要 ====================
    def _result_summary(self, mode, result):
        v, m = result
        if mode == 'mp3':
            return "MP3 已生成。" if m else "MP3 转换失败。"
        elif mode == 'cover':
            return "封面已下载。" if v else "封面下载失败。"
        elif mode == 'all':
            return "视频、封面、简介已下载。" if v else "处理失败。"
        else:
            return "视频已下载。" if v else "视频下载失败。"

    # ==================== 统一入口 ====================
    def run(self, input_str, mode='video'):
        if mode == 'intro':
            return self._handle_intro(input_str)
        if self._is_uploader_url(input_str):
            return self._handle_uploader(input_str, mode)
        return self._handle_video_url(input_str, mode)


# ==================== 拖拽模式 ====================
def process_drop_path(path, tool, overwrite=False):
    if not os.path.exists(path):
        print(f"路径不存在: {path}")
        return
    if os.path.isfile(path):
        if path.lower().endswith('.mp4'):
            mp3_path = os.path.splitext(path)[0] + '.mp3'
            if not overwrite and os.path.exists(mp3_path):
                print(f"已有同名 MP3，跳过: {os.path.basename(mp3_path)}")
                return
            tool._convert_mp4_to_mp3(path)
        else:
            print(f"跳过（不是 MP4）: {os.path.basename(path)}")
    elif os.path.isdir(path):
        print(f"正在扫描文件夹: {path}")
        count = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.mp4'):
                    full = os.path.join(root, file)
                    mp3_path = os.path.splitext(full)[0] + '.mp3'
                    if not overwrite and os.path.exists(mp3_path):
                        print(f"已有同名 MP3，跳过: {file}")
                        continue
                    tool._convert_mp4_to_mp3(full)
                    count += 1
        if count == 0:
            print("这个文件夹里没有找到需要转换的 MP4 文件。")


def drag_drop_mode(args):
    tool = BilibiliTool(SAVE_PATH)
    print("=" * 50)
    print("MP4 转 MP3 工具")
    print("=" * 50)
    print("拖进来的内容：")
    for a in args:
        print(f"  - {a}")
    print("-" * 50)
    for arg in args:
        process_drop_path(arg, tool)
    print("-" * 50)
    print("全部处理完毕，按回车键关闭窗口。")
    input()


# ==================== 交互模式 ====================
def interactive_mode():
    print("=" * 55)
    print("BiliTools")
    print("=" * 55)
    print("链接 → 下载视频（合集会自动全部下载，UP主主页会下载全部作品）")
    print("链接 mp3 → 下载视频，自动转成 MP3，然后删掉视频")
    print("链接 cover → 只下载这张视频的封面图片")
    print("链接 intro → 提取视频简介，保存成 txt 文件")
    print("链接 all → 下载视频 + 封面 + 简介（不转 MP3）")
    print("       （合集或UP主会把对应全部都提取出来）")
    print(f"保存路径：  {SAVE_PATH}")
    print("（合集会单独建一个以合集名字命名的子文件夹）")
    print("（UP 主会单独建一个以 UP 主名字命名的子文件夹）")
    print("=" * 55)
    if not FFMPEG_PATH:
        print("提示：没有找到 ffmpeg，MP3 功能暂时不能用。")
    if not YTDLP_PATH:
        print("提示：没有找到 yt-dlp，UP主功能可能受限。")
        print("      建议安装：pip install yt-dlp")
    print("想结束的时候，直接关掉这个窗口就行了。")
    print()

    tool = BilibiliTool(SAVE_PATH)

    while True:
        try:
            raw = input("输入指令: ").strip()
            if not raw:
                print("你什么都没输入，再试一次吧。")
                continue

            mode = 'video'
            input_str = raw
            parts = raw.rsplit(None, 1)

            if len(parts) == 2:
                last = parts[1].lower()
                if last in BilibiliTool.MODES:
                    before = parts[0].rsplit(None, 1)
                    if len(before) == 2 and before[1].lower() in BilibiliTool.MODES:
                        print("错误：一次只能用一种模式。")
                        continue
                    mode = last
                    input_str = parts[0].strip()

            if not input_str:
                print("好像只输入了模式，没看到链接。")
                continue

            print("-" * 55)
            tool.run(input_str, mode=mode)
            print("-" * 55)

        except KeyboardInterrupt:
            print("\n\n好的，程序退出。")
            break
        except Exception as e:
            print(f"\n这次没成功: {e}")
            print("检查一下链接是不是完整的，或者稍后再试试。")


# ==================== 主入口 ====================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        drag_drop_mode(sys.argv[1:])
    else:
        interactive_mode()