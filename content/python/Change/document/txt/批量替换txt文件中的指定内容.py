import os

def replace_content(directory, old_content, new_content):
    # 遍历指定目录
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.txt'):
                # 拼接完整的文件路径
                filepath = os.path.join(foldername, filename)
                # 打开并读取文件内容
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # 替换指定的内容
                    content = content.replace(old_content, new_content)
                    # 写回文件
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                print(f"文件'{filename}'中的'{old_content}'已替换为'{new_content}'。")

# 输入目录路径
directory_path = os.getcwd()
# 输入要替换的字符串
old_content = input("请输入要替换的内容：")
# 输入替换后的字符串
new_content = input("请输入新的内容：")
replace_content(directory_path, old_content, new_content)
print("操作完成。")

# ============================================================
# 脚本说明：批量替换 TXT 文件中的指定内容
# ============================================================
#
# 功能：
#   从当前工作目录开始，递归遍历所有 .txt 文件；
#   读取每个文件的内容，将用户指定的旧字符串替换为新字符串；
#   然后直接写回原文件，并在控制台打印替换提示。
#
# 执行流程：
#   1. 以 os.getcwd() 作为根目录；
#   2. 通过 input 获取要替换的旧内容 old_content；
#   3. 通过 input 获取替换后的新内容 new_content；
#   4. replace_content 使用 os.walk 递归遍历目录：
#        - 筛选出以 .txt 结尾的文件；
#        - 以 UTF-8 编码读取文件全部内容；
#        - 使用 str.replace 将 old_content 全部替换为 new_content；
#        - 以 UTF-8 编码写回原文件；
#        - 打印每个被处理的文件名和替换信息；
#   5. 输出“操作完成”。
#
# 注意事项：
#   - 直接修改原文件，没有备份，替换错误无法撤销；
#   - 不跳过任何文件夹，包括 .git、__pycache__、系统目录等；
#   - 只处理 .txt 文件，但不会判断文件是否真的是文本；
#   - 编码固定为 UTF-8，遇到其他编码可能读取失败或乱码；
#   - 替换是全局的、大小写敏感的，且会替换所有出现位置；
#   - 没有预览和确认步骤，输入后立即执行；
#   - 如果脚本所在目录中有大量 txt 文件，可能会误改无关文件；
#   - 如果 old_content 为空字符串，可能导致在每个字符间插入新内容；
#   - 没有异常处理，某个文件读写失败可能导致脚本中断。
#
# 可能的改进：
#   - 增加备份机制，或先写入临时文件再替换；
#   - 增加 dry-run 预览模式，列出将要修改的文件和替换次数；
#   - 让用户确认后再执行；
#   - 支持排除指定文件夹，如 .git、聊天记录等；
#   - 支持正则表达式替换；
#   - 支持大小写不敏感替换；
#   - 记录替换日志，方便回滚；
#   - 处理多种编码，或使用 errors='ignore'；
#   - 支持命令行参数传入目录、旧内容和新内容。
#
# 一句话总结：
#   这是一个递归批量替换当前目录下所有 TXT 文件内容的脚本，
#   使用简单但风险较高，直接修改原文件且无备份、无预览、无过滤。
# ============================================================