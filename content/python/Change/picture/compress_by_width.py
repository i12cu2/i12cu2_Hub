# ==================== 用户设置区（只改这里） ====================

# 压缩后的图片保存到哪个文件夹（不存在会自动创建）
OUTPUT_DIR = r"C:\Users\Admin\Desktop\Images"

# JPG/WebP 压缩质量：1~100，越小越省空间、画质越差
JPEG_QUALITY = 50

# 图片最大宽度（像素）：超过此宽度会自动等比缩小
# 设 0 表示不缩小
MAX_WIDTH = 1080

# 是否保留原来的文件夹结构？
# False = 所有图片平铺到 OUTPUT_DIR（重名自动加 _1、_2）
# True  = 按拖入文件夹的相对路径放到 OUTPUT_DIR 下
KEEP_STRUCTURE = False

# 遇到这些格式直接复制，不做压缩处理
SKIP_COMPRESS_EXT = ('.gif', '.svg', '.ico', '.bmp', '.tif', '.tiff')

# 会去搜索的图片扩展名（拖文件夹时按这个找图）
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp',
              '.tif', '.tiff', '.svg', '.ico'}

# ===============================================================


import sys, os, subprocess, importlib, site, shutil, traceback, datetime
from pathlib import Path

LOG = Path(__file__).with_name("compress_log.txt")

def log(msg):
    print(msg)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now():%H:%M:%S}] {msg}\n")
    except Exception:
        pass

def ensure_pillow():
    try:
        from PIL import Image
        return Image
    except ImportError:
        pass

    log("未检测到 Pillow，正在自动安装，请稍等...")

    try:
        user_site = site.getusersitepackages()
        if user_site and user_site not in sys.path:
            site.addsitedir(user_site)
    except Exception:
        pass

    attempts = [
        [sys.executable, "-m", "pip", "install", "--upgrade", "Pillow"],
        [sys.executable, "-m", "pip", "install", "--user", "--upgrade", "Pillow"],
        [sys.executable, "-m", "ensurepip", "--upgrade"],
        [sys.executable, "-m", "pip", "install", "--user", "--upgrade", "Pillow"],
    ]

    for cmd in attempts:
        try:
            log("执行：" + " ".join(cmd))
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.stdout:
                log(r.stdout.strip()[-500:])
            if r.stderr:
                log(r.stderr.strip()[-500:])
        except Exception as e:
            log(f"命令执行异常：{e}")

        try:
            importlib.invalidate_caches()
            if site.getusersitepackages() not in sys.path:
                site.addsitedir(site.getusersitepackages())
            from PIL import Image
            log("Pillow 安装成功。")
            return Image
        except ImportError:
            continue

    log("自动安装 Pillow 失败。请手动在 cmd 运行：")
    log(f'  "{sys.executable}" -m pip install Pillow')
    input("\n按回车退出...")
    sys.exit(1)


Image = ensure_pillow()

OUTPUT_DIR = Path(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR_RESOLVED = OUTPUT_DIR.resolve()

def human(n):
    for u in ['B', 'KB', 'MB', 'GB']:
        if n < 1024:
            return f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}TB"

def is_inside_output(p: Path) -> bool:
    """判断文件是否在输出目录里，避免把上次的结果再压一遍。"""
    try:
        p.resolve().relative_to(OUTPUT_DIR_RESOLVED)
        return True
    except ValueError:
        return False

def collect_images(raw_paths):
    """把拖入的文件/文件夹展开成图片列表，自动去重。"""
    seen = set()
    files = []
    for p in raw_paths:
        p = Path(p)
        if p.is_dir():
            log(f"扫描文件夹：{p}")
            for f in sorted(p.rglob('*')):
                if not f.is_file():
                    continue
                if f.suffix.lower() not in IMAGE_EXTS:
                    continue
                if is_inside_output(f):
                    continue
                key = os.path.normcase(str(f.resolve()))
                if key in seen:
                    continue
                seen.add(key)
                files.append(f)
        elif p.is_file():
            if p.suffix.lower() not in IMAGE_EXTS:
                log(f"跳过非图片：{p.name}")
                continue
            if is_inside_output(p):
                log(f"跳过输出目录内的文件：{p.name}")
                continue
            key = os.path.normcase(str(p.resolve()))
            if key in seen:
                continue
            seen.add(key)
            files.append(p)
    return files

def guess_base_dir(raw_paths):
    """猜一个基准目录，用于 KEEP_STRUCTURE 时计算相对路径。"""
    try:
        dirs = [str(p if Path(p).is_dir() else Path(p).parent) for p in raw_paths]
        return Path(os.path.commonpath(dirs))
    except Exception:
        return None

def make_dst(src: Path, base_dir):
    """计算输出路径，处理重名。"""
    if KEEP_STRUCTURE and base_dir:
        try:
            rel = src.relative_to(base_dir)
            dst = OUTPUT_DIR / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
        except ValueError:
            dst = OUTPUT_DIR / src.name
    else:
        dst = OUTPUT_DIR / src.name

    if not dst.exists():
        return dst

    stem, suffix = dst.stem, dst.suffix
    i = 1
    while True:
        cand = dst.with_name(f"{stem}_{i}{suffix}")
        if not cand.exists():
            return cand
        i += 1

def compress_one(src: Path, base_dir):
    dst = make_dst(src, base_dir)
    ext = src.suffix.lower()

    if ext in SKIP_COMPRESS_EXT:
        shutil.copy2(src, dst)
        log(f"{src.name}: 直接复制（此格式不压缩）")
        return src.stat().st_size, dst.stat().st_size

    with Image.open(src) as im:
        if MAX_WIDTH and im.width > MAX_WIDTH:
            ratio = MAX_WIDTH / im.width
            im = im.resize((MAX_WIDTH, int(im.height * ratio)), Image.LANCZOS)

        if ext in ('.jpg', '.jpeg'):
            im = im.convert('RGB')
            im.save(dst, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        elif ext == '.png':
            im.save(dst, 'PNG', optimize=True)
        elif ext == '.webp':
            im.save(dst, 'WEBP', quality=JPEG_QUALITY)
        else:
            im.save(dst)

    old, new = src.stat().st_size, dst.stat().st_size
    if new >= old:
        dst.unlink()
        shutil.copy2(src, dst)
        new = old

    log(f"{src.name}: {human(old)} -> {human(new)}  (省 {(1-new/old)*100:.1f}%)")
    return old, new

def main():
    raw = [p for p in sys.argv[1:] if p.strip()]
    if not raw:
        log("没有收到路径。请把图片或文件夹拖到 run.bat 上，或一行一个粘贴路径，空行结束：")
        lines = []
        while True:
            line = input().strip().strip('"')
            if not line:
                break
            lines.append(line)
        raw = lines

    if not raw:
        log("没有输入。")
        return

    files = collect_images(raw)
    if not files:
        log("没有找到可处理的图片。")
        return

    base_dir = guess_base_dir(raw)
    log(f"共找到 {len(files)} 张图片")
    log(f"输出目录：{OUTPUT_DIR}")
    log(f"质量：{JPEG_QUALITY}，最大宽度：{MAX_WIDTH if MAX_WIDTH else '不限'}，保留结构：{KEEP_STRUCTURE}")

    total_old = total_new = 0
    ok = fail = 0
    for f in files:
        try:
            o, n = compress_one(f, base_dir)
            ok += 1
        except Exception as e:
            log(f"{f.name}: 失败 - {e}")
            fail += 1
            continue
        total_old += o
        total_new += n

    log("--- 汇总 ---")
    log(f"成功：{ok}，失败：{fail}")
    log(f"原总大小：{human(total_old)}")
    log(f"压缩后：{human(total_new)}")
    if total_old:
        log(f"总共省：{human(total_old-total_new)} ({(1-total_new/total_old)*100:.1f}%)")

if __name__ == '__main__':
    try:
        main()
    except Exception:
        log("程序出错了：\n" + traceback.format_exc())
    input("\n按回车退出...")