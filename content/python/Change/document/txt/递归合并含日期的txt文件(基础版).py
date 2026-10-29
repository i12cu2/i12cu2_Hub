import os
import re
from datetime import datetime

def find_txt_files(folder_path):
    """递归查找所有txt文件"""
    txt_files = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith('.txt'):
                file_path = os.path.join(root, filename)
                txt_files.append(file_path)
    return txt_files

def extract_date_from_filename(filename):
    """从文件名中提取日期"""
    # 匹配YYYY.MM.DD或YYYY.M.D格式
    match = re.search(r'(\d{4})\.(\d{1,2})\.(\d{1,2})', filename)
    if match:
        year, month, day = map(int, match.groups())
        try:
            return datetime(year, month, day)
        except ValueError:
            return None
    return None

def merge_txt_files(folder_path, output_file="merged.txt"):
    # 获取所有txt文件路径
    txt_files = find_txt_files(folder_path)
    
    if not txt_files:
        print("未找到txt文件")
        return
    
    # 存储文件信息：(日期, 文件路径, 文件名)
    file_data = []
    
    for file_path in txt_files:
        filename = os.path.basename(file_path)
        file_date = extract_date_from_filename(filename)
        
        if not file_date:
            continue  # 跳过不含有效日期的文件
            
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"读取文件 {file_path} 失败: {e}")
            continue
            
        file_data.append((file_date, file_path, content, filename))
    
    if not file_data:
        print("未找到包含有效日期的txt文件")
        return
    
    # 按日期排序
    file_data.sort(key=lambda x: x[0])
    
    # 写入合并文件
    with open(output_file, 'w', encoding='utf-8') as out:
        for _, _, content, filename in file_data:
            # 去除文件名中的.txt扩展名
            display_name = os.path.splitext(filename)[0]
            
            # 写入文件名分隔线
            out.write(f"\n\n{'=' * 50}\n")
            out.write(f"文件: {display_name}\n")
            out.write(f"{'=' * 50}\n\n")
            # 写入文件内容
            out.write(content)
            out.write('\n')  # 文件末尾添加换行
    
    print(f"已合并 {len(file_data)} 个文件到 {output_file}")

if __name__ == "__main__":
    target_folder = r"C:\Users\chru\Desktop\Crown_of_Tokamak"
    if os.path.isdir(target_folder):
        output_name = "merged.txt"
        merge_txt_files(target_folder, output_name)
    else:
        print("错误：无效的文件夹路径")

# ============================================================
# 脚本说明：递归合并含日期的 TXT 文件（基础版）
# ============================================================
#
# 功能：
#   从指定目录 folder_path 开始，递归查找所有 .txt 文件；
#   从文件名中提取 YYYY.M.D 或 YYYY.MM.DD 格式的日期；
#   只合并文件名含有效日期的 txt 文件，并按日期升序排序；
#   最终输出到 merged.txt，每个文件前带分隔线和文件名。
#
# 执行流程：
#   1. find_txt_files 使用 os.walk 递归遍历 folder_path，
#      收集所有 .txt 文件路径，不跳过任何文件夹；
#   2. extract_date_from_filename 用正则匹配文件名中的日期，
#      并用 datetime 验证有效性，无效则返回 None；
#   3. merge_txt_files 对每个 txt 文件：
#        - 提取文件名并解析日期，跳过无有效日期的文件；
#        - 以 UTF-8 读取内容，读取失败则打印错误并跳过；
#        - 保存为 (日期, 文件路径, 内容, 文件名)；
#   4. 按日期升序排序；
#   5. 写入输出文件：
#        - 每个文件前输出 50 个 '=' 组成的分隔线；
#        - 显示文件名（去掉 .txt 扩展名）；
#        - 写入文件内容，末尾补换行；
#   6. main 中检查硬编码路径是否存在，存在则调用合并，
#      输出到 merged.txt，否则打印错误。
#
# 注意事项：
#   - 只合并文件名中含 YYYY.M.D 或 YYYY.MM.DD 的 txt 文件；
#   - 递归所有子目录，不跳过任何文件夹（如 .git、聊天记录等）；
#   - 输出文件名为 merged.txt，如果它位于目标目录内且扩展名为 .txt，
#     可能会被再次读入，导致内容重复膨胀；
#   - 文件编码固定为 UTF-8，遇到其他编码可能读取失败；
#   - 读取异常会捕获并跳过，但写入异常未处理；
#   - 文件顺序按日期升序，日期相同的文件顺序取决于 os.walk 的遍历顺序；
#   - target_folder 是硬编码路径，换环境需要手动修改；
#   - 输出中不包含源目录、合并时间、相对路径等头部信息。
#
# 可能的改进：
#   - 排除输出文件自身，避免自包含；
#   - 增加 IGNORE_FOLDERS 过滤，跳过不需要的目录；
#   - 支持命令行参数传入目标目录和输出文件名；
#   - 支持更多日期格式，如 YYYY-MM-DD、YYYY_MM_DD；
#   - 尝试多种编码读取，或使用 errors='ignore'；
#   - 增加写入异常处理；
#   - 使用 pathlib 简化路径操作；
#   - 在合并文件头部添加合并时间、源目录、文件数量等统计信息。
#
# 一句话总结：
#   这是一个递归合并指定目录下含日期文件名的 TXT 文件的脚本，
#   按日期排序，输出带文件名分隔线的合并文件，但不过滤文件夹、
#   不含头部统计信息，适合简单场景。
# ============================================================