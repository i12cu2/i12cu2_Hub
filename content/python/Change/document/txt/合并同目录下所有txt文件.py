import os

def merge_txt_files(root_dir):
    # 列出目录中的所有.txt文件
    txt_files = [f for f in os.listdir(root_dir) if os.path.splitext(f)[1] == '.txt']
    
    # 逐个打开并读取.txt文件
    merged_content = ''
    for txt_file in txt_files:
        #merged_content+=txt_file.split('.')[0]+'\n'
        with open(os.path.join(root_dir, txt_file), 'r', encoding='utf-8') as f:
            merged_content += f.read() # + '\n'  # 将文件内容合并，每个文件内容后添加一个换行符

    # 将合并后的内容写入新的.txt文件
    with open(os.path.join(root_dir, 'merged.txt'), 'w', encoding='utf-8') as f:
        f.write(merged_content)

# 调用函数，传入脚本根目录
root_dir = r"C:\Users\chru\Desktop\Unreal_Engine_Develop_Notes\content\杂谈\托卡马克之冠\知乎主页" #os.path.dirname(__file__)
merge_txt_files(root_dir)

print('done to merge txt')

# ============================================================
# 脚本说明：合并同目录下的所有 .txt 文件
# ============================================================
#
# 功能：
#   将指定目录 root_dir 下所有 .txt 文件的内容按 os.listdir 返回的顺序
#   依次拼接，最终写入同目录下的 merged.txt 文件。
#
# 执行流程：
#   1. 使用 os.listdir(root_dir) 列出目录下所有条目；
#   2. 通过 os.path.splitext 过滤出扩展名为 .txt 的文件；
#   3. 逐个打开这些 .txt 文件，以 UTF-8 编码读取全部内容；
#   4. 将内容累加到一个字符串 merged_content 中；
#   5. 把 merged_content 写入 root_dir/merged.txt。
#
# 注意事项：
#   - 只处理 root_dir 根层，不递归子文件夹。
#   - 文件顺序取决于 os.listdir 的返回顺序，通常不是按名称或日期排序。
#   - 没有在文件之间添加任何分隔符或文件名标记，内容会直接首尾相连。
#   - 如果 merged.txt 已经存在，它也会被当作待合并的 .txt 文件之一，
#     导致旧内容被再次读入并写入，可能造成内容重复膨胀。
#   - 没有异常处理，如果某个文件读取失败（编码错误、权限问题等），
#     整个脚本会中断。
#   - root_dir 是硬编码路径，换环境需要手动修改。
#
# 可能的改进：
#   - 排除 merged.txt 自身，避免自包含。
#   - 对文件名排序，或按修改时间、文件名中的日期排序。
#   - 在文件之间添加分隔线和文件名标题。
#   - 使用 try/except 处理读取和写入错误。
#   - 支持递归子目录，或通过命令行参数传入路径。
#   - 使用 pathlib 或 glob 模块让代码更简洁。
#
# 一句话总结：
#   这是一个最简单的同目录 TXT 合并脚本，适合快速拼接少量文本，
#   但缺乏排序、分隔和防自包含机制，使用时需注意输出文件是否已存在。
# ============================================================