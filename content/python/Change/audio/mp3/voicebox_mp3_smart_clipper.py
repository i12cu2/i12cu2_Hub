# -*- coding: utf-8 -*-
"""
Voicebox MP3 Smart Clipper
将 mp3 拖动到本脚本上运行，自动截取 25~30 秒的非静音片段。
"""

import sys
import os
import re
import traceback
import subprocess
from datetime import datetime

# ============ 配置 ============
FFMPEG_PATH  = r"C:\Program File\ffmpeg\bin\ffmpeg.exe"    # 注意核对 Program Files
FFPROBE_PATH = r"C:\Program File\ffmpeg\bin\ffprobe.exe"

MIN_DURATION      = 25.0
MAX_DURATION      = 29.9
TARGET_DURATION   = 27.5
SILENCE_THRESHOLD = "-40dB"
SILENCE_MIN_LEN   = 0.5

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clipper_log.txt")
# ==============================


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def pause():
    """无论如何都暂停，让窗口不闪退"""
    try:
        input("\n按回车键退出...")
    except EOFError:
        # 极少数情况（比如 stdin 被关闭）
        import time
        time.sleep(5)


def check_binaries():
    ok = True
    for name, p in (("ffmpeg", FFMPEG_PATH), ("ffprobe", FFPROBE_PATH)):
        if not os.path.isfile(p):
            log(f"[错误] 找不到 {name}: {p}")
            ok = False
    return ok


def get_duration(path):
    cmd = [FFPROBE_PATH, "-v", "error",
           "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1",
           path]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return float(out.stdout.strip())


def detect_silence(path):
    cmd = [FFMPEG_PATH, "-hide_banner", "-i", path,
           "-af", f"silencedetect=noise={SILENCE_THRESHOLD}:d={SILENCE_MIN_LEN}",
           "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    text = out.stderr

    starts = [float(m) for m in re.findall(r"silence_start:\s*([\d.]+)", text)]
    ends   = [float(m) for m in re.findall(r"silence_end:\s*([\d.]+)",   text)]

    silences = []
    for i, s in enumerate(starts):
        e = ends[i] if i < len(ends) else None
        silences.append((s, e))
    return silences


def find_best_segment(path, total):
    if total <= MAX_DURATION:
        return 0.0, total

    silences = detect_silence(path)

    non_silent = []
    prev = 0.0
    for s, e in silences:
        if s > prev:
            non_silent.append((prev, s))
        if e is None:
            prev = total
        else:
            prev = max(prev, e)
    if prev < total:
        non_silent.append((prev, total))

    candidates = [(s, e) for s, e in non_silent if e - s >= TARGET_DURATION]

    if candidates:
        best = max(candidates, key=lambda x: x[1] - x[0])
        mid = (best[0] + best[1]) / 2.0
        start = mid - TARGET_DURATION / 2.0
        if start < best[0]:
            start = best[0]
        if start + TARGET_DURATION > best[1]:
            start = best[1] - TARGET_DURATION
        return start, start + TARGET_DURATION

    start = max(0.0, (total - TARGET_DURATION) / 2.0)
    return start, start + TARGET_DURATION


def process_file(path):
    path = os.path.abspath(path.strip('"').strip("'"))  # 去掉拖拽时可能带的引号
    if not os.path.isfile(path):
        log(f"[跳过] 不是有效文件: {path}")
        return
    if not path.lower().endswith(".mp3"):
        log(f"[跳过] 非 mp3 文件: {path}")
        return

    dir_name  = os.path.dirname(path)
    base_name = os.path.basename(path)
    name, ext = os.path.splitext(base_name)

    try:
        total = get_duration(path)
    except Exception as e:
        log(f"[错误] 读取时长失败: {base_name} -> {e}")
        return

    log(f"[处理] {base_name}  总时长 = {total:.2f}s")

    start, end = find_best_segment(path, total)

    if end - start > MAX_DURATION:
        end = start + MAX_DURATION
    if end > total:
        end = total
        start = max(0.0, end - TARGET_DURATION)

    duration = end - start

    if duration < MIN_DURATION:
        log(f"  [警告] 截取长度 {duration:.2f}s 低于 {MIN_DURATION}s")

    start_i = int(round(start))
    end_i   = int(round(end))

    out_name = f"{name}_{start_i}_{end_i}{ext}"
    out_path = os.path.join(dir_name, out_name)

    counter = 1
    while os.path.exists(out_path):
        out_name = f"{name}_{start_i}_{end_i}_{counter}{ext}"
        out_path = os.path.join(dir_name, out_name)
        counter += 1

    cmd = [
        FFMPEG_PATH, "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{start:.3f}",
        "-i", path,
        "-t",  f"{duration:.3f}",
        "-c:a", "libmp3lame", "-q:a", "2",
        out_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if r.returncode != 0:
        log(f"  [错误] ffmpeg 执行失败: {r.stderr.strip()}")
        return

    log(f"  [完成] -> {out_name}   ({start:.2f}s ~ {end:.2f}s, 共 {duration:.2f}s)")


def run():
    log("=" * 60)
    log("Voicebox MP3 Smart Clipper 启动")

    if not check_binaries():
        log("ffmpeg / ffprobe 路径有问题，请修改脚本顶部的 FFMPEG_PATH / FFPROBE_PATH")
        return

    if len(sys.argv) < 2:
        log("未接收到文件。请把 mp3 文件拖动到本脚本上运行。")
        return

    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    log(f"共 {len(files)} 个文件待处理")

    for f in files:
        try:
            process_file(f)
        except Exception as e:
            log(f"[异常] {os.path.basename(f)} -> {e}")
            log(traceback.format_exc())

    log("全部处理完成！")


if __name__ == "__main__":
    try:
        run()
    except Exception:
        # 任何未捕获异常都写进日志并显示
        err = traceback.format_exc()
        print(err)
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(err + "\n")
        except Exception:
            pass
    finally:
        pause()