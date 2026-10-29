import re
import html
import pathlib

# 以脚本所在目录为基准
base = pathlib.Path(__file__).resolve().parent
src = base / "ReadmeEdit.md"

print("读取文件：", src)
if not src.exists():
    raise SystemExit(f"文件不存在：{src}")

text = src.read_text(encoding="utf-8")

# 找到 ```text ... ``` 代码块
pattern = re.compile(r"```text\n(.*?)\n```", re.S)
m = pattern.search(text)
if not m:
    raise SystemExit("没有找到 ```text 代码块")

block = m.group(1)

# 先转义 HTML 特殊字符，避免 & < > 破坏结构
escaped = html.escape(block, quote=True)

# 逐行处理
new_lines = []
for line in escaped.split("\n"):
    # 匹配：前缀树形符号 + 描述 + URL
    # 前缀：空格和 │ ├ └ ─ 等树形符号
    m2 = re.match(r"^([\s│├└─]*)(.*?)\s*(https?://\S+)\s*$", line)
    if m2:
        prefix = m2.group(1)      # 树形符号和缩进
        desc = m2.group(2).strip()  # 描述文字
        url = m2.group(3)         # 链接
        if not desc:
            desc = url
        new_line = f'{prefix}<a href="{url}">{desc}</a>'
    else:
        new_line = line
    new_lines.append(new_line)

# 用 <pre> 包裹，保持树形结构
new_block = "<pre>\n" + "\n".join(new_lines) + "\n</pre>"

# 替换原代码块
new_text = text[:m.start()] + new_block + text[m.end():]

out = src.with_name("Readme.md")
out.write_text(new_text, encoding="utf-8")
print(f"已生成：{out}")