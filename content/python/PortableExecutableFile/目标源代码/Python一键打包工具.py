#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 一键打包工具

特性：
  - 拖放 .py 文件即可打包成 EXE
  - 自动检测 / 安装 PyInstaller
  - 支持多文件批量打包
  - 支持单文件/单目录、控制台/窗口模式、图标、隐藏导入、附加数据
  - 实时转发打包日志，同时写入日志文件
  - 构建产物放系统临时目录，源目录只留下最终 EXE
  - 只清理自己创建的临时目录，不会误删源目录的 build/__pycache__

用法：
  python make_exe.py your_script.py
  python make_exe.py a.py b.py --windowed
  python make_exe.py script.py --icon app.ico --hidden-import requests --timeout 900
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path

DEFAULT_TIMEOUT = 600

_logger = logging.getLogger("py2exe")


# --------------------------------------------------------------------------- #
# 日志
# --------------------------------------------------------------------------- #
def setup_logger(log_file: Path | None) -> None:
    _logger.setLevel(logging.DEBUG)
    _logger.handlers.clear()
    _logger.propagate = False

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(console)

    if log_file:
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(str(log_file), encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            _logger.addHandler(fh)
        except Exception as exc:
            print(f"警告：无法创建日志文件 {log_file}: {exc}")


def info(msg: str = "") -> None:
    _logger.info(msg)


def warn(msg: str) -> None:
    _logger.warning(msg)


def error(msg: str = "") -> None:
    _logger.error(msg)


# --------------------------------------------------------------------------- #
# 通用工具
# --------------------------------------------------------------------------- #
def format_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def path_size(p: Path) -> str:
    try:
        if p.is_file():
            return format_size(p.stat().st_size)
        total = sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
        return format_size(total) + "（目录合计）"
    except Exception:
        return "未知"


def open_path(path: str) -> None:
    try:
        if os.name == "nt":
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=False)
        else:
            subprocess.run(["xdg-open", path], check=False)
    except Exception as exc:
        warn(f"无法打开目录 {path}: {exc}")


# --------------------------------------------------------------------------- #
# PyInstaller 检测 / 安装
# --------------------------------------------------------------------------- #
def find_pyinstaller() -> list[str] | None:
    """返回可用于调用 PyInstaller 的命令前缀；未找到返回 None。"""
    candidates: list[list[str]] = [[sys.executable, "-m", "PyInstaller"]]
    exe = shutil.which("pyinstaller")
    if exe:
        candidates.append([exe])

    for prefix in candidates:
        try:
            r = subprocess.run(
                prefix + ["--version"],
                capture_output=True, text=True, timeout=30,
            )
        except Exception:
            continue
        if r.returncode == 0:
            lines = (r.stdout or r.stderr or "").strip().splitlines()
            ver = lines[0] if lines else "unknown"
            info(f"✓ 使用 PyInstaller {ver}（{' '.join(prefix)}）")
            return prefix
    return None


def install_pyinstaller() -> bool:
    if getattr(sys, "frozen", False):
        error("✗ 当前程序是打包后的 EXE，无法自动安装 PyInstaller。")
        error("  请先安装 Python，再执行：pip install pyinstaller")
        return False

    try:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode != 0:
            error("✗ 未检测到可用的 pip，无法自动安装 PyInstaller。")
            return False
    except Exception:
        error("✗ 未检测到可用的 pip，无法自动安装 PyInstaller。")
        return False

    info("未检测到 PyInstaller，正在安装（可能需要几分钟）...")
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"],
            capture_output=True, text=True, timeout=600,
        )
    except Exception as exc:
        error(f"✗ 安装 PyInstaller 出错: {exc}")
        return False

    if r.returncode != 0:
        error("✗ PyInstaller 安装失败。")
        tail = "\n".join((r.stderr or r.stdout or "").splitlines()[-15:])
        if tail:
            error(tail)
        return False

    info("✓ PyInstaller 安装成功")
    return True


# --------------------------------------------------------------------------- #
# 流式执行子进程
# --------------------------------------------------------------------------- #
def run_streaming(cmd: list[str], cwd: Path, timeout: int) -> tuple[int, list[str], list[str]]:
    """执行命令，实时转发 stdout/stderr，返回 (returncode, stdout_lines, stderr_lines)。"""
    info("正在打包，请稍候...")

    process = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        errors="replace",
    )

    stdout_lines: list[str] = []
    stderr_lines: list[str] = []

    def reader(pipe, sink: list[str], level: int) -> None:
        try:
            with pipe:
                for raw in iter(pipe.readline, ""):
                    line = raw.rstrip()
                    if line:
                        sink.append(line)
                        _logger.log(level, line)
        except Exception as exc:
            _logger.debug("读取输出出错: %s", exc)

    t_out = threading.Thread(target=reader, args=(process.stdout, stdout_lines, logging.INFO), daemon=True)
    t_err = threading.Thread(target=reader, args=(process.stderr, stderr_lines, logging.ERROR), daemon=True)
    t_out.start()
    t_err.start()

    try:
        returncode = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        error(f"✗ 打包超时（>{timeout}s），正在终止进程...")
        process.terminate()
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        returncode = -1
    finally:
        t_out.join(timeout=10)
        t_err.join(timeout=10)

    return returncode, stdout_lines, stderr_lines


# --------------------------------------------------------------------------- #
# 单个文件打包
# --------------------------------------------------------------------------- #
def build_one(src: str, args: argparse.Namespace, prefix: list[str]) -> tuple[Path, float] | None:
    src_path = Path(src).expanduser().resolve()

    if not src_path.exists():
        error(f"✗ 文件不存在: {src_path}")
        return None
    if not src_path.is_file():
        error(f"✗ 不是普通文件: {src_path}")
        return None
    if src_path.suffix.lower() != ".py":
        error(f"✗ 只支持 .py 文件: {src_path.name}")
        return None

    src_dir = src_path.parent
    stem = src_path.stem
    exe_name = stem + (".exe" if os.name == "nt" else "")

    # 每个文件独立临时目录：build/spec 都放这里，源目录只留最终 EXE
    temp_root = Path(tempfile.mkdtemp(prefix="py2exe_"))
    try:
        (temp_root / "build").mkdir(parents=True, exist_ok=True)
        (temp_root / "spec").mkdir(parents=True, exist_ok=True)

        cmd = list(prefix)
        cmd += [
            "--onefile" if args.onefile else "--onedir",
            "--windowed" if args.windowed else "--console",
            "--clean",
            "--noconfirm",
            "--noupx",
            "--name", stem,
            "--distpath", str(src_dir),
            "--workpath", str(temp_root / "build"),
            "--specpath", str(temp_root / "spec"),
        ]
        if args.icon:
            cmd += ["--icon", args.icon]
        for item in args.hidden_import or []:
            cmd += ["--hidden-import", item]
        for item in args.add_data or []:
            cmd += ["--add-data", item]

        cmd.append(str(src_path))

        info(f"源文件  : {src_path}")
        info(f"输出目录: {src_dir}")
        info(f"输出名称: {stem}")
        info(f"命令    : {subprocess.list2cmdline(cmd)}")
        info("-" * 60)

        start = time.time()
        returncode, _, stderr_lines = run_streaming(cmd, cwd=src_dir, timeout=args.timeout)
        elapsed = time.time() - start

        if returncode != 0:
            error(f"✗ 打包失败（返回码 {returncode}，耗时 {elapsed:.1f}s）")
            tail = "\n".join(stderr_lines[-20:])
            if tail:
                error("错误摘要（最后 20 行）：")
                error(tail)
            return None

        if args.onefile:
            output = src_dir / exe_name
        else:
            output = src_dir / stem
            candidate = output / exe_name
            if candidate.exists():
                output = candidate

        if not output.exists():
            error(f"✗ PyInstaller 返回成功但未找到输出: {output}")
            return None

        info("-" * 60)
        info("✓ 打包成功！")
        info(f"输出: {output}")
        info(f"大小: {path_size(output)}")
        info(f"耗时: {elapsed:.1f}s")
        return output, elapsed
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


# --------------------------------------------------------------------------- #
# 参数 / 主流程
# --------------------------------------------------------------------------- #
def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="make_exe",
        description="Python 一键打包工具：把 .py 文件打包成 EXE",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python make_exe.py script.py\n"
            "  python make_exe.py a.py b.py --windowed\n"
            "  python make_exe.py script.py --icon app.ico --hidden-import requests --timeout 900\n"
        ),
    )
    parser.add_argument("files", nargs="*", help="要打包的 .py 文件（可多个，支持拖放）")

    g1 = parser.add_mutually_exclusive_group()
    g1.add_argument("--onefile", dest="onefile", action="store_true", default=True,
                    help="打包为单个 EXE（默认）")
    g1.add_argument("--onedir", dest="onefile", action="store_false",
                    help="打包为目录（含依赖文件）")

    g2 = parser.add_mutually_exclusive_group()
    g2.add_argument("--console", dest="windowed", action="store_false", default=False,
                    help="显示控制台窗口（默认）")
    g2.add_argument("--windowed", "--noconsole", dest="windowed", action="store_true",
                    help="不显示控制台窗口（GUI 程序）")

    parser.add_argument("--icon", help="EXE 图标（.ico）")
    parser.add_argument("--hidden-import", action="append", dest="hidden_import",
                        help="额外的隐藏导入（可重复）")
    parser.add_argument("--add-data", action="append", dest="add_data",
                        help="附加数据文件，格式 SOURCE:DEST（Windows 可用 SOURCE;DEST）")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"单个文件打包超时秒数（默认 {DEFAULT_TIMEOUT}）")
    parser.add_argument("--no-install", action="store_true",
                        help="不自动安装 PyInstaller")
    parser.add_argument("--open", dest="open_after", action="store_true",
                        help="打包完成后打开输出目录")
    parser.add_argument("--log", help="日志文件路径（默认写到临时目录）")
    parser.add_argument("--pause", action="store_true", help="结束前暂停")
    parser.add_argument("--no-pause", action="store_true", help="结束前不暂停")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示更详细日志")
    return parser.parse_args(argv)


def do_pause() -> None:
    try:
        stdin = getattr(sys, "stdin", None)
        if stdin is not None and stdin.isatty():
            input("\n按回车键退出...")
    except (EOFError, KeyboardInterrupt):
        pass


def maybe_pause(args: argparse.Namespace) -> None:
    if args.no_pause:
        return
    if args.pause:
        do_pause()
        return
    # 拖放 exe 运行、或双击无参数运行时暂停，方便查看结果
    if getattr(sys, "frozen", False) or not args.files:
        do_pause()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    log_file = Path(args.log).expanduser() if args.log else (
        Path(tempfile.gettempdir()) / "py2exe_logs" / f"pack_{datetime.now():%Y%m%d_%H%M%S}.log"
    )
    setup_logger(log_file)
    if args.verbose:
        for handler in _logger.handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                handler.setLevel(logging.DEBUG)

    info("=" * 60)
    info("Python 一键打包工具")
    info(f"Python : {sys.version.split()[0]}")
    info(f"平台   : {sys.platform}")
    info(f"模式   : {'frozen EXE' if getattr(sys, 'frozen', False) else 'Python 脚本'}")
    info(f"日志   : {log_file}")
    info("=" * 60)

    if sys.version_info < (3, 8):
        warn(f"⚠ 当前 Python {sys.version.split()[0]} 较旧，建议升级到 3.8+")

    if not args.files:
        info("")
        info("使用方法：")
        info("  1) 把 .py 文件拖放到本程序上；或")
        info("  2) python make_exe.py your_script.py")
        info("")
        info("常用选项：")
        info("  --windowed          GUI 程序不显示控制台窗口")
        info("  --onedir            打包成目录而不是单文件")
        info("  --icon app.ico      设置 EXE 图标")
        info("  --timeout 900       设置超时（秒）")
        info("")
        info("用 -h/--help 查看全部选项。")
        maybe_pause(args)
        return 0

    if args.icon:
        icon_path = Path(args.icon).expanduser().resolve()
        if not icon_path.exists():
            error(f"✗ 图标文件不存在: {icon_path}")
            maybe_pause(args)
            return 1
        args.icon = str(icon_path)

    prefix = find_pyinstaller()
    if prefix is None:
        if args.no_install:
            error("✗ 未找到 PyInstaller，且指定了 --no-install。")
            maybe_pause(args)
            return 1
        if not install_pyinstaller():
            error("请手动安装后重试：pip install pyinstaller")
            maybe_pause(args)
            return 1
        prefix = find_pyinstaller()
        if prefix is None:
            error("✗ 安装后仍未检测到 PyInstaller。")
            maybe_pause(args)
            return 1

    results: list[tuple[str, tuple[Path, float] | None]] = []
    for index, src in enumerate(args.files, start=1):
        info("")
        info("=" * 60)
        info(f"[{index}/{len(args.files)}] {src}")
        info("=" * 60)
        try:
            result = build_one(src, args, prefix)
        except KeyboardInterrupt:
            error("用户中断。")
            break
        except Exception:
            error("打包过程中出现异常：")
            error(traceback.format_exc())
            result = None
        results.append((src, result))

    info("")
    info("=" * 60)
    info("汇总")
    info("=" * 60)
    success = 0
    for src, result in results:
        if result is not None:
            success += 1
            out_path, _ = result
            info(f"  ✓ {src}  ->  {out_path}  ({path_size(out_path)})")
        else:
            info(f"  ✗ {src}")
    info("")
    info(f"成功 {success}/{len(results)}")

    if args.open_after and success:
        dirs = sorted({str(Path(src).expanduser().resolve().parent) for src, r in results if r})
        for d in dirs:
            open_path(d)

    maybe_pause(args)
    return 0 if results and success == len(results) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n已取消。")
        sys.exit(130)