"""
压缩包批量解压工具
功能：将拖动的文件/文件夹中的7Z/ZIP/RAR压缩包解压到同名文件夹
"""

import os
import sys
import subprocess
import tempfile
import shutil
import base64
from tqdm import tqdm

# ===================== 嵌入式二进制数据 =====================
#BIN_7Z = """\

#BIN_7Z_DLL = """\

#BIN_7Z_SFX = """\

#BIN_7ZCON_SFX = """\

#BIN_WINRAR = """\

#BIN_RAR = """\

#BIN_UNRAR = """\

#BIN_RAREXT_DLL = """\


# ======================================================

class PortableCompressionTools:
    """
    便携式压缩工具管理器
    """
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="extraction_tools_")
        self.extracted_files = {}
        self.is_initialized = False
        
    def extract_binary(self, binary_data, filename):
        """
        从二进制数据提取文件到临时目录
        """
        if not binary_data:
            return None
            
        file_path = os.path.join(self.temp_dir, filename)
        try:
            # 解码base64数据
            clean_base64 = binary_data.replace('\n', '').replace(' ', '')
            file_data = base64.b64decode(clean_base64)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            return file_path
        except Exception as e:
            print(f"提取文件 {filename} 时出错: {str(e)}")
            return None
    
    def initialize_tools(self):
        """
        初始化工具，提取所有必要的二进制文件
        """
        if self.is_initialized:
            return True
            
        print("初始化便携式解压工具...")
        
        try:
            # 7z文件映射
            sevenzip_files = [
                ("7z.exe", BIN_7Z),
                ("7z.dll", BIN_7Z_DLL),
                ("7z.sfx", BIN_7Z_SFX),
                ("7zCon.sfx", BIN_7ZCON_SFX),
            ]
            
            # WinRAR文件映射
            winrar_files = [
                ("WinRAR.exe", BIN_WINRAR),
                ("Rar.exe", BIN_RAR),
                ("UnRAR.exe", BIN_UNRAR),
                ("RarExt.dll", BIN_RAREXT_DLL),
            ]
            
            # 提取7z文件
            print("提取7z工具...")
            for filename, binary_data in sevenzip_files:
                if binary_data:
                    file_path = self.extract_binary(binary_data, filename)
                    if file_path:
                        self.extracted_files[filename] = file_path
                        print(f"  ✓ {filename}")
            
            # 提取WinRAR文件
            print("提取WinRAR工具...")
            for filename, binary_data in winrar_files:
                if binary_data:
                    file_path = self.extract_binary(binary_data, filename)
                    if file_path:
                        self.extracted_files[filename] = file_path
                        print(f"  ✓ {filename}")
            
            # 验证必要文件
            if "7z.exe" not in self.extracted_files or "7z.dll" not in self.extracted_files:
                print("错误: 缺少必要7z文件")
                return False
            
            if "WinRAR.exe" not in self.extracted_files:
                print("错误: 缺少必要WinRAR文件")
                return False
            
            self.is_initialized = True
            print("✓ 工具初始化完成")
            return True
            
        except Exception as e:
            print(f"✗ 工具初始化失败: {str(e)}")
            return False
    
    def get_7z_path(self):
        """获取7z.exe路径"""
        return self.extracted_files.get("7z.exe")
    
    def get_winrar_path(self):
        """获取WinRAR.exe路径"""
        return self.extracted_files.get("WinRAR.exe")
    
    def get_unrar_path(self):
        """获取UnRAR.exe路径"""
        return self.extracted_files.get("UnRAR.exe")
    
    def cleanup(self):
        """清理临时文件"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except:
            pass

def create_silent_process_config():
    """创建静默运行配置"""
    startupinfo = None
    creationflags = 0
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        creationflags = subprocess.CREATE_NO_WINDOW
    return startupinfo, creationflags

def extract_archive(archive_path, output_dir, tools_manager):
    """
    解压压缩包到指定目录
    """
    startupinfo, creationflags = create_silent_process_config()
    
    # 获取文件扩展名
    ext = os.path.splitext(archive_path)[1].lower()
    
    try:
        # 根据文件类型选择解压工具
        if ext in ['.7z', '.zip']:
            # 使用7z解压7z和zip文件
            sevenzip_path = tools_manager.get_7z_path()
            if not sevenzip_path:
                return False, "7z工具未找到"
            
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # 7z解压命令
            subprocess.run(
                [sevenzip_path, "x", archive_path, f"-o{output_dir}", "-y", "-spd"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            return True, ""
            
        elif ext == '.rar':
            # 使用WinRAR解压rar文件
            winrar_path = tools_manager.get_winrar_path()
            if not winrar_path:
                return False, "WinRAR工具未找到"
            
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # WinRAR解压命令
            subprocess.run(
                [winrar_path, "x", "-ibck", "-idq", "-o+", archive_path, output_dir],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            return True, ""
        else:
            return False, f"不支持的文件格式: {ext}"
            
    except subprocess.CalledProcessError as e:
        return False, f"解压过程错误: {e.returncode}"
    except Exception as e:
        return False, f"意外错误: {str(e)}"

def process_file(file_path, tools_manager):
    """
    处理单个文件
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return False, f"文件不存在: {file_path}"
    
    # 获取文件扩展名
    ext = os.path.splitext(file_path)[1].lower()
    
    # 只处理压缩文件
    if ext not in ['.7z', '.zip', '.rar']:
        return True, f"跳过: 非压缩文件 - {os.path.basename(file_path)}"
    
    # 生成输出目录名（与压缩包同名，不带扩展名）
    output_dir = os.path.splitext(file_path)[0]
    
    # 如果输出目录已存在，添加序号
    counter = 1
    original_output_dir = output_dir
    while os.path.exists(output_dir):
        output_dir = f"{original_output_dir}_{counter}"
        counter += 1
    
    # 执行解压
    try:
        success, message = extract_archive(file_path, output_dir, tools_manager)
        if success:
            return True, f"成功: {os.path.basename(file_path)} -> {os.path.basename(output_dir)}"
        else:
            return False, f"解压失败: {os.path.basename(file_path)} - {message}"
    except Exception as e:
        return False, f"异常: 处理文件时出错 - {os.path.basename(file_path)} - {str(e)}"

def process_directory(directory):
    """
    处理目录中的所有压缩文件
    返回找到的文件列表
    """
    archive_files = []
    try:
        # 检查目录是否存在
        if not os.path.exists(directory):
            print(f"错误: 目录不存在 - {directory}")
            return archive_files
        
        # 遍历目录中的所有压缩文件
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.7z', '.zip', '.rar')):
                    full_path = os.path.join(root, file)
                    if os.path.isfile(full_path):
                        archive_files.append(full_path)
        
        return archive_files
    except Exception as e:
        print(f"异常: 处理目录时出错 - {directory} - {str(e)}")
        return archive_files

def main():
    """主函数"""
    tools_manager = None
    
    try:
        # 初始化便携式工具
        tools_manager = PortableCompressionTools()
        if not tools_manager.initialize_tools():
            print("错误: 无法初始化解压工具")
            print("请确保二进制变量已正确填充")
            input("按任意键退出...")
            return
        
        # 处理命令行参数
        if len(sys.argv) > 1:
            # 收集所有需要处理的文件
            all_files = []
            
            # 处理每个参数
            for i in range(1, len(sys.argv)):
                target_path = sys.argv[i]
                print(f"扫描: {target_path}")
                
                if os.path.isfile(target_path):
                    # 如果是文件，直接添加到处理列表
                    all_files.append(target_path)
                elif os.path.isdir(target_path):
                    # 如果是目录，扫描目录中的所有压缩文件
                    dir_files = process_directory(target_path)
                    all_files.extend(dir_files)
                else:
                    print(f"错误: 路径不存在 - {target_path}")
            
            # 去重
            all_files = list(set(all_files))
            
            if not all_files:
                print("未找到需要解压的7Z/ZIP/RAR文件")
                return
            
            print(f"找到 {len(all_files)} 个需要解压的文件")
            
            # 使用进度条处理每个文件
            success_count = 0
            with tqdm(all_files, desc="解压进度", unit="file", colour="green") as pbar:
                for file_path in pbar:
                    base_name = os.path.basename(file_path)
                    pbar.set_postfix(file=base_name[:20])  # 显示前20个字符
                    
                    # 处理文件
                    success, message = process_file(file_path, tools_manager)
                    
                    # 处理结果
                    if success:
                        if "成功" in message:
                            success_count += 1
                        pbar.write(f"[✓] {message}")
                    else:
                        pbar.write(f"[✕] {message}")
            
            # 输出统计信息
            print(f"\n解压完成！成功解压 {success_count}/{len(all_files)} 个文件")
        else:
            print("请将压缩包文件或文件夹拖放到此程序上运行")
            print("\n使用方法:")
            print("1. 将7Z/ZIP/RAR文件/文件夹拖放到此程序图标上")
            print("2. 程序将自动解压到同名文件夹")
            print("3. 如果同名文件夹已存在，会自动添加序号")
            print("4. 非压缩文件将被跳过")
            
    except Exception as e:
        print(f"程序异常: {str(e)}")
    finally:
        # 清理临时文件
        if tools_manager:
            tools_manager.cleanup()

if __name__ == "__main__":
    main()
    print("\n程序执行完毕，按任意键退出...")
    input()