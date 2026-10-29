# -*- coding: utf-8 -*-
"""
项目来源于 https://github.com/great-os/AlexTranscript 对其transcript文件夹进行的二次整理
将 B 站转写 md 文件：
    1. 读取内容，提取标题、发布日期、对话正文
    2. 重命名为  YYYY.MM.DD + 标题 + .txt
    3. 按年份移动到同级 "YYYY" 文件夹
    4. txt 内容只保留对话正文（去掉 [时间戳]： 前缀）

用法：
    先把 DRY_RUN 设为 True 预览一遍，确认输出没问题后改成 False 真正执行。
"""

import re
from pathlib import Path

# ===================== 配置区 =====================
BASE_DIR = r"C:\Users\Admin\Desktop\口播\AlexTranscript-main\transcript"
DRY_RUN = False   # True = 只预览不修改；False = 真正执行
# ==================================================

# 一级标题：# 标题
TITLE_RE = re.compile(r'^\s*#\s+(.+?)\s*$', re.MULTILINE)

# 发布日期：- **发布日期**: 2025-01-26 23:44:43
DATE_RE = re.compile(r'\*\*发布日期\*\*\s*[:：]\s*(\d{4})\s*[-./年]\s*(\d{1,2})\s*[-./月]\s*(\d{1,2})')

# 对话行：- [00:00:00]：哎呀哎...
DIALOG_LINE_RE = re.compile(r'^\s*-\s*\[[\d:.\s]+\]\s*[:：]?\s*(.*)$')

# 文件名非法字符（Windows）
INVALID_CHARS = r'<>:"/\|?*'


def sanitize(name: str) -> str:
    """去掉文件名中不允许的字符，并压缩空白"""
    for ch in INVALID_CHARS:
        name = name.replace(ch, '_')
    return re.sub(r'\s+', ' ', name).strip()


def parse_md(text: str):
    """返回 (title, date_str, [对话行, ...]) 或 None"""
    title_m = TITLE_RE.search(text)
    if not title_m:
        return None
    title = title_m.group(1).strip()

    date_m = DATE_RE.search(text)
    if not date_m:
        return None
    y, mo, d = date_m.groups()
    year = f"{int(y):04d}"
    date_str = f"{year}.{int(mo):02d}.{int(d):02d}"

    dialogues = []
    for line in text.splitlines():
        m = DIALOG_LINE_RE.match(line)
        if m:
            content = m.group(1).strip()
            if content:
                dialogues.append(content)

    return title, date_str, dialogues


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    i = 1
    while True:
        p = path.with_name(f"{path.stem}_{i}{path.suffix}")
        if not p.exists():
            return p
        i += 1


def main():
    base = Path(BASE_DIR)
    if not base.is_dir():
        print(f"❌ 目录不存在：{base}")
        return

    files = [f for f in sorted(base.iterdir())
             if f.is_file() and f.suffix.lower() in ('.md', '.markdown', '.txt')]

    if not files:
        print("没有找到 md 文件。")
        return

    ok, skipped = 0, 0
    for f in files:
        try:
            text = f.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            text = f.read_text(encoding='utf-8-sig', errors='ignore')

        parsed = parse_md(text)
        if parsed is None:
            print(f"⚠️  [跳过] 无法解析：{f.name}")
            skipped += 1
            continue

        title, date_str, dialogues = parsed
        if not dialogues:
            print(f"⚠️  [跳过] 无对话内容：{f.name}")
            skipped += 1
            continue

        new_name = sanitize(f"{date_str}{title}") + ".txt"
        year = date_str[:4]
        target_dir = base / year
        target = unique_path(target_dir / new_name)

        print(f"{f.name}\n    ➜ {year}\\{target.name}  （{len(dialogues)} 行对话）")
        ok += 1

        if DRY_RUN:
            continue

        target_dir.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(dialogues) + "\n", encoding='utf-8')
        f.unlink()   # 删除原 md 文件（若想保留原文件，把这行注释掉）

    print("\n" + "=" * 60)
    print(f"{'【预览模式】' if DRY_RUN else '【已执行】'}  "
          f"可处理 {ok} 个，跳过 {skipped} 个")
    if DRY_RUN:
        print("确认无误后，把 DRY_RUN 改成 False 再运行一次即可。")


if __name__ == '__main__':
    main()