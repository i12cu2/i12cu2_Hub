# -*- coding: utf-8 -*-
"""
插件SubBatch来源于 https://microsoftedge.microsoft.com/addons/detail/enimmdlbbcfhcefiafpfekjlikohcgmn

将【b站博主名字】系列 txt 文件：
    1. 重命名为  YYYY.MM.DD + 中间内容 + .txt
    2. 按年份移动到同级 "YYYY" 文件夹

用法：
    先把 DRY_RUN 设为 True 预览一遍，确认输出没问题后改成 False 真正执行。
"""

import re
from pathlib import Path

# ===================== 配置区 =====================
BASE_DIR = r"C:\Users\Admin\Desktop\杰哥观察者模式启动中"
DRY_RUN = False  # True = 只预览不修改；False = 真正执行
# ==================================================

# 匹配【...】块
BRACKET_RE = re.compile(r'【([^【】]*)】')
# 匹配日期：2023-11-06 / 2023.11.6 / 2023/11/06 / 2023年11月6日 都可以
DATE_RE = re.compile(r'(\d{4})\s*[-./年]\s*(\d{1,2})\s*[-./月]\s*(\d{1,2})\s*日?')

# 用于剔除中间内容首尾的分隔符
SEP_CHARS = ' \t\u3000—-–—~～·、,，。:：'


def build_new_name(stem: str):
    """
    根据文件名主干(stem, 不含扩展名)生成新名字。
    成功返回 (year, new_name)；无法解析返回 None。
    """
    brackets = list(BRACKET_RE.finditer(stem))
    if not brackets:
        return None

    # 从右往左找最后一个「内容中含日期」的【...】，作为基准时间
    date_br, date_m = None, None
    for br in reversed(brackets):
        m = DATE_RE.search(br.group(1))
        if m:
            date_br, date_m = br, m
            break
    if date_m is None:
        return None

    y, mo, d = date_m.groups()
    year = f"{int(y):04d}"
    new_date = f"{year}.{int(mo):02d}.{int(d):02d}"   # 自动补零

    first = brackets[0]
    if date_br.start() < first.end():
        # 极端情况：日期就是最左边那个【...】
        middle = stem[date_br.end():]
    else:
        # 取第一个【...】与日期【...】之间的内容
        middle = stem[first.end():date_br.start()]

    middle = middle.strip(SEP_CHARS)

    return year, f"{new_date}{middle}.txt"


def unique_path(path: Path) -> Path:
    """目标文件已存在时，自动加 _1 / _2 后缀，避免覆盖"""
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
             if f.is_file() and f.suffix.lower() == '.txt']

    if not files:
        print("没有找到 txt 文件。")
        return

    ok, skipped = 0, 0
    for f in files:
        res = build_new_name(f.stem)
        if res is None:
            print(f"⚠️  [跳过] 无法解析：{f.name}")
            skipped += 1
            continue

        year, new_name = res
        target_dir = base / year
        target = unique_path(target_dir / new_name)

        print(f"{f.name}\n    ➜ {year}\\{target.name}")
        ok += 1

        if DRY_RUN:
            continue

        target_dir.mkdir(parents=True, exist_ok=True)
        f.rename(target)   # 同盘移动直接用 rename

    print("\n" + "=" * 60)
    print(f"{'【预览模式】' if DRY_RUN else '【已执行】'}  "
          f"可处理 {ok} 个，跳过 {skipped} 个")
    if DRY_RUN:
        print("确认无误后，把 DRY_RUN 改成 False 再运行一次即可。")


if __name__ == '__main__':
    main()

"""

📝 SubBatch - 字幕批量处理工具

🌟 插件介绍
SubBatch 是一个强大的浏览器扩展插件，专为批量获取和导出视频字幕而设计，暂时只支持 B 站视频。它可以帮助用户轻松获取单个或批量视频的字幕数据，并支持导出为 SRT 或 TXT 格式的字幕文件，特别适合用于 AI 知识库建设（如 NotebookLM）、学习笔记整理或视频内容分析。

💡 特别适合将 B 站优质内容转化为个人 AI 知识库的素材，一键批量导出纯文本格式，无需手动复制粘贴！

✨ 主要功能

* 🎬 批量获取字幕：同时处理多个 B 站视频的字幕数据
* 📥 多种导入方式：支持单个视频 URL、当前页面地址、整个收藏夹导入
* 📤 灵活导出格式：

  * SRT 格式：包含时间轴的标准字幕格式，适合播放器使用
  * TXT 格式：纯文本格式，完美适配 NotebookLM 等 AI 知识库
* 📊 视频列表管理：表格化展示所有导入的视频，清晰直观
* 🔄 批量处理：一键操作，节省时间
* 🔒 隐私保护：本地处理数据，不上传到第三方服务器

📋 使用指南

🚀 快速开始

1. 安装扩展后，点击浏览器工具栏中的 SubBatch 图标
2. 在弹出的侧边栏中使用以下任一方法添加视频：

   * 输入 B 站视频 URL 并点击“添加到表格”
   * 在 B 站视频页面点击“获取视频地址”按钮
   * 在 B 站收藏夹页面点击“获取收藏夹”按钮

🧩 界面和按钮说明

顶部按钮区：

* 📚 使用文档：打开本插件的详细使用文档和教程
* 💬 反馈问题：前往反馈页面提交使用中遇到的问题
* ❤️ 赞助我：如果您觉得插件有用，可以支持开发者
* 🎬 获取视频地址：获取当前浏览的 B 站视频页面 URL
* 📂 获取收藏夹：获取当前浏览的 B 站收藏夹内所有视频
* 🌟 关注我：前往开发者的 B 站主页关注

输入区域：

* Cookie：输入 B 站 Cookie 以获取需要登录才能观看的视频字幕
* 视频地址：输入单个 B 站视频 URL，点击右侧“添加到表格”按钮添加
* 收藏夹地址：输入 B 站收藏夹 URL，点击右侧“获取收藏夹视频”按钮批量导入

视频列表操作按钮：

* 🎬 获取字幕：批量获取表格中所有视频的字幕数据
* 📥 导出字幕：将已获取字幕的视频批量导出为 SRT 或 TXT 格式
* 🗑️ 清空表格：清空当前表格中的所有视频数据

视频列表表格字段说明：

* 序号：视频在列表中的位置
* 视频标题：点击可跳转到对应视频页面
* 作者：视频的 UP 主
* 字幕状态：显示字幕获取状态（未获取/获取中/已获取/获取失败）
* 操作：可删除单个视频

🔍 详细使用流程

1️⃣ 获取视频字幕

1. 通过上述任一方式将视频添加到表格
2. 点击“获取字幕”按钮开始批量获取字幕
3. 进度条会显示当前处理进度
4. 获取完成后，字幕状态会更新为“已获取”或显示错误信息

2️⃣ 导出字幕文件

1. 确保至少有一个视频的字幕状态为“已获取”
2. 点击“导出字幕”按钮
3. 在弹出的格式选择框中选择导出格式：

   * SRT 格式：包含时间轴和序号的标准字幕格式，适合播放器
   * TXT 格式：仅包含文本内容，适合 AI 知识库使用
4. 选择后将自动下载为 ZIP 文件，内含所有字幕文件

3️⃣ 使用收藏夹批量导入

1. 打开 B 站收藏夹页面
2. 点击“获取收藏夹地址”按钮或手动复制 URL 到输入框
3. 点击“获取收藏夹视频”按钮
4. 所有视频将被添加到表格中

💡 使用技巧

* 选择合适的格式：

  * 用于视频剪辑或研究时间轴 → 选择 SRT
  * 用于 AI 知识库或文本分析 → 选择 TXT
* 批量处理：统一添加再统一处理字幕，提高效率
* 字幕筛选：获取失败的可单独重试
* Cookie 设置：需要登录的视频需设置 Cookie 才能获取字幕

🛠️ 常见问题

* 字幕获取失败：检查视频是否有字幕，或尝试设置 Cookie
* 收藏夹导入失败：确认收藏夹 URL 是否正确，必要时设置 Cookie
* 下载的 ZIP 文件打不开：请使用最新版解压软件，或确认下载是否完整

📊 AI 知识库应用场景
SubBatch 特别适合与 NotebookLM 等 AI 工具结合使用，用于构建个人知识库：

1. 使用 SubBatch 批量导出感兴趣 B 站视频的字幕为 TXT 文件
2. 将 TXT 文件导入 NotebookLM 或其他 AI 笔记工具
3. 使用 AI 提取要点、总结内容、整理笔记
4. 建立个人专题知识库，随时随地检索与学习

"""