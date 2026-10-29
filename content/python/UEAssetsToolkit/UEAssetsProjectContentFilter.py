r"""
处理 D:\660p1.84T\Projects\overProject 下的每个项目单位（一级子文件夹）：

1. 深度查找 .uproject 文件，取其同级目录下的 Content 文件夹。
2. 列出 Content 内的子文件夹，排除 MARKER_DIRS 中的名字。
3. 若剩余子文件夹数量恰好为 1，则把整个项目单位文件夹
   移动到 TARGET_DIR；否则原地不动。

说明：
- 移动对象是整个一级子文件夹本身，不拆分内部结构。
- 目标目录已有同名文件夹时，自动追加 _1、_2 后缀，避免覆盖。
- 终端只输出命中的单位信息，未命中的不打印。
"""

import os
import shutil
import sys
from pathlib import Path

# ================= 配置区 =================
SOURCE_DIR = Path(r"D:\660p1.84T\Projects\overProject")        # 项目单位根目录
TARGET_DIR = Path(r"D:\660p1.84T\Projects\overProjectSingle")  # 命中的单位移动目标（请按需修改）

UPROJECT_EXTENSION = ".uproject"

MARKER_DIRS = {
    "__externalactors__",
    "__externalobjects__",
    "collections",
    "developers",
    "startercontent",
    "splash"
}   # 排除名单（统一小写比较）

DRY_RUN = False   # 先 True 预览，确认无误后再改为 False 实际执行
# =========================================


def find_uproject(unit: Path):
    """深度查找 unit 下第一个 .uproject 文件，返回完整路径；找不到返回 None"""
    for dirpath, _, filenames in os.walk(unit):
        for f in filenames:
            if f.lower().endswith(UPROJECT_EXTENSION):
                return Path(dirpath) / f
    return None


def find_content_folder(uproject: Path):
    """在 .uproject 同级目录下查找名为 Content 的文件夹（不区分大小写）"""
    parent = uproject.parent
    for d in parent.iterdir():
        if d.is_dir() and d.name.lower() == "content":
            return d
    return None


def unique_dest(dest_dir: Path, name: str) -> Path:
    """目标已存在同名文件夹时，自动加 _1、_2 后缀，避免覆盖"""
    dest = dest_dir / name
    if not dest.exists():
        return dest
    i = 1
    while True:
        cand = dest_dir / f"{name}_{i}"
        if not cand.exists():
            return cand
        i += 1


def main():
    if not SOURCE_DIR.is_dir():
        print(f"[错误] 源目录不存在：{SOURCE_DIR}")
        sys.exit(1)

    if not DRY_RUN:
        TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # 排除目标目录本身，防止误扫、误移
    target_resolved = TARGET_DIR.resolve()

    units = sorted(
        (p for p in SOURCE_DIR.iterdir()
         if p.is_dir() and p.resolve() != target_resolved),
        key=lambda p: p.name.lower(),
    )

    moved_count = 0
    failed_count = 0

    for unit in units:
        # 1. 定位 .uproject
        uproject = find_uproject(unit)
        if uproject is None:
            continue

        # 2. 定位同级 Content
        try:
            content = find_content_folder(uproject)
        except Exception as e:
            print(f"[扫描失败] {unit.name} -> {e}")
            failed_count += 1
            continue
        if content is None:
            continue

        # 3. 过滤排除名单，统计有效子文件夹
        try:
            subfolders = [d for d in content.iterdir() if d.is_dir()]
        except Exception as e:
            print(f"[扫描失败] {unit.name} -> {e}")
            failed_count += 1
            continue

        valid = [d for d in subfolders if d.name.lower() not in MARKER_DIRS]
        if len(valid) != 1:
            continue

        # 4. 命中：移动整个项目单位
        dest = unique_dest(TARGET_DIR, unit.name)

        if DRY_RUN:
            print(f"[命中] {unit.name}")
            print(f"       Content：{content}")
            print(f"       唯一有效子文件夹：{valid[0].name}")
            print(f"       将移动到： {dest}   （预览模式，未移动）")
            moved_count += 1
            continue

        try:
            shutil.move(str(unit), str(dest))
            print(f"[命中] 已移动：{unit.name}  ->  {dest}")
            moved_count += 1
        except Exception as e:
            print(f"[命中] 移动失败：{unit.name} -> {e}")
            failed_count += 1

    print("-" * 70)
    print(f"完成。命中并{'预览' if DRY_RUN else '移动'}：{moved_count} 个；失败：{failed_count} 个。")
    if DRY_RUN:
        print("当前为预览模式，未做任何实际改动。确认后请将 DRY_RUN 改为 False。")


if __name__ == "__main__":
    main()