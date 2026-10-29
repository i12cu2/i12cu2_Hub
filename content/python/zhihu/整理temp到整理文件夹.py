import os
import re

def parse_markdown_file(input_file_path, output_directory=None):
    """
    解析 Markdown 文件，根据标题创建文本文件
    
    参数:
        input_file_path (str): 输入的 Markdown 文件路径
        output_directory (str): 输出文件的目录（可选，默认为当前目录）
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_file_path):
        print(f"错误: 文件 '{input_file_path}' 不存在")
        return
    
    # 设置输出目录
    if output_directory is None:
        output_directory = os.getcwd()  # 默认为当前工作目录
    else:
        # 确保输出目录存在
        os.makedirs(output_directory, exist_ok=True)
    
    # 读取文件内容
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return
    
    # 使用正则表达式匹配标题和代码块
    pattern = r'(.+?)\n```(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        print("未找到符合格式的内容")
        return
    
    # 处理每个匹配项
    for title, code_content in matches:
        # 清理标题和内容中的空白字符
        title = title.strip()
        code_content = code_content.strip()
        
        # 创建安全的文件名（移除所有非字母数字字符，保留空格并用下划线替代）
        safe_title = re.sub(r'[^\w\s-]', '', title)  # 移除非字母数字、非空格、非连字符的字符
        safe_title = re.sub(r'[-\s]+', '_', safe_title)  # 将空格和连字符替换为下划线
        safe_title = safe_title.rstrip('_')  # 移除末尾的下划线
        
        # 如果标题处理后为空，使用默认名称
        if not safe_title:
            safe_title = "untitled"
        
        file_name = f"{safe_title}.txt"
        output_path = os.path.join(output_directory, file_name)
        
        # 检查文件是否已存在
        file_exists = os.path.exists(output_path)
        
        # 写入文件
        try:
            mode = 'a' if file_exists else 'w'
            with open(output_path, mode, encoding='utf-8') as output_file:
                if file_exists:
                    output_file.write('\n\n')  # 添加分隔空行
                output_file.write(code_content)
            
            action = "追加到" if file_exists else "创建"
            print(f"{action}文件: {output_path}")
            
        except Exception as e:
            print(f"写入文件 '{output_path}' 时出错: {e}")

if __name__ == "__main__":
    # 获取当前Python文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 基于当前目录设置相对路径
    input_md_path = os.path.join(current_dir, "temp.txt")
    output_dir = os.path.join(current_dir, "整理")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 解析文件
    parse_markdown_file(input_md_path, output_dir)