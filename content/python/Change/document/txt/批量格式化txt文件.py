import os
import re

def reformat_text_files(directory_path):
    # 创建保存处理后文件的目录
    output_dir = os.path.join(directory_path, "reformatted")
    os.makedirs(output_dir, exist_ok=True)
    
    # 递归遍历目录中的所有文件
    for root, dirs, files in os.walk(directory_path):
        # 跳过输出目录本身
        if os.path.abspath(root) == os.path.abspath(output_dir):
            continue
            
        for filename in files:
            if filename.lower().endswith('.txt'):
                file_path = os.path.join(root, filename)
                
                # 计算相对路径用于输出目录结构
                rel_path = os.path.relpath(root, directory_path)
                if rel_path == ".":
                    rel_path = ""
                
                # 创建对应的输出子目录
                output_subdir = os.path.join(output_dir, rel_path)
                os.makedirs(output_subdir, exist_ok=True)
                
                # 读取文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='gbk') as file:
                            content = file.read()
                    except:
                        print(f"无法解码文件: {file_path}")
                        continue
                
                # 删除所有空白字符（包括空格、换行、制表符等）
                content = re.sub(r'\s+', '', content)
                
                # 按中文标点重新换行
                # 处理常见标点：句号、问号、感叹号、省略号、分号、逗号等
                content = re.sub(r'([。？！…；])([^”’])', r'\1\n\n\2', content)  # 后引号特殊情况处理
                content = re.sub(r'([。？！…；][”’])([^"])', r'\1\n\n\2', content)
                # content = re.sub(r'([，、])', r'\1\n', content)
                
                # 保存处理后的文件
                output_path = os.path.join(output_subdir, filename)
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"已处理: {os.path.join(rel_path, filename)}")

if __name__ == "__main__":
    target_directory = r"C:\Users\chru\Desktop\merge"
    
    if not os.path.isdir(target_directory):
        print("错误: 指定的路径不是目录或不存在")
    else:
        reformat_text_files(target_directory)
        print("\n处理完成! 所有文件已保存到'reformatted'目录中，保持原有目录结构")

# ============================================================
# 脚本说明：批量格式化 TXT 文件（去空白 + 按中文标点重分段）
# ============================================================
#
# 功能：
#   递归遍历指定目录下的所有 .txt 文件，读取内容后：
#     1. 删除所有空白字符（空格、换行、制表符等）；
#     2. 按中文标点（。？！…；）重新换行，每个标点后加两个换行；
#     3. 将处理后的文件保存到原目录下的 reformatted 子目录中，
#        并保持原有的目录结构。
#
# 执行流程：
#   1. 在目标目录下创建输出目录 reformatted；
#   2. 使用 os.walk 递归遍历目标目录，跳过输出目录本身；
#   3. 对每个 .txt 文件：
#        - 计算相对路径，在输出目录中创建对应的子目录；
#        - 读取文件：先尝试 UTF-8，失败则尝试 GBK，
#          再失败则打印“无法解码”并跳过；
#        - 用 re.sub(r'\s+', '', content) 删除所有空白字符；
#        - 用正则替换在中文标点后插入两个换行：
#            ([。？！…；])([^”’])  ->  \1\n\n\2
#            ([。？！…；][”’])([^"]) ->  \1\n\n\2
#          （逗号、顿号等替换被注释掉，未启用）
#        - 将结果以 UTF-8 写入输出目录中的对应文件；
#        - 打印已处理的相对路径。
#   4. 主程序检查硬编码的目标目录是否存在，
#      存在则调用 reformat_text_files，否则打印错误。
#
# 注意事项：
#   - 只处理 .txt 文件，且只处理目标目录及其子目录；
#   - 会删除所有空白字符，因此原有的段落、缩进、空行全部丢失，
#     完全依靠中文标点重新分段；
#   - 重新分段只针对 。？！…； 这几个标点，逗号、顿号等未启用；
#   - 输出目录为 reformatted，保持相对目录结构；
#   - 编码只尝试 UTF-8 和 GBK，其他编码会跳过并提示；
#   - 没有备份机制，输出目录中的同名文件会被直接覆盖；
#   - 如果再次运行脚本，reformatted 目录内的文件可能被再次处理，
#     因为跳过逻辑只跳过了输出目录的根，未跳过其子目录；
#   - 写入操作没有异常处理，磁盘满或权限问题可能导致中断；
#   - 目标目录是硬编码路径，换环境需要手动修改。
#
# 可能的改进：
#   - 排除输出目录及其所有子目录，避免重复处理；
#   - 增加 dry-run 预览模式，先显示将要修改的文件；
#   - 保留部分空白，例如只压缩连续空白，而不是全部删除；
#   - 支持更多标点，或让用户自定义分段标点；
#   - 支持命令行参数传入目标目录和输出目录；
#   - 增加写入异常处理；
#   - 处理英文标点（. ? ! ;）或中英文混合；
#   - 对输出文件添加处理时间、源文件路径等头部信息。
#
# 一句话总结：
#   这是一个递归读取 TXT 文件、删除所有空白、按中文标点重新分段，
#   并将结果保存到 reformatted 目录（保持目录结构）的格式化脚本。
# ============================================================