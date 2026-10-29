"""
ZIP/7Z转RAR + RAR冗余文件删除 综合工具 - 便携版
功能1: 将拖动的ZIP/7Z文件转换为RAR格式（使用嵌入式7z和WinRAR）
功能2: 对所有RAR文件（包括转换生成的）删除内部指定的冗余文件/文件夹（使用嵌入式WinRAR）
无需安装任何软件，所有功能内置在单一Python文件中
"""

import os
import sys
import subprocess
import tempfile
import shutil
import base64
import csv
from pathlib import Path
import argparse
from datetime import datetime
import time
from collections import namedtuple

# ===================== 用户配置区域 =====================

# 代码2配置：需要删除的文件夹/文件名称模式（支持部分匹配）
delete_patterns = ["Saved", "Intermediate", "Build", "Binaries", ".vs", ".svn", "DerivedDataCache","使用教程【必看】",
                   "Read me.rar", "更多免费软件素材1.jpg",
                   "首页-虚幻4资源站-淘宝网.url", "2d素材库-传奇素材包-素材免费下载.url", "2d素材库素材免费下载.url", "3d模型-爱给模型库-素材免费下载.url","3d模型素材免费下载.url","51render.url",
                   "虚幻(UE)素材免费下载.url", "源码素材免费下载.url","CG3DA - 免费下载各类精品CG资源 .url",
                   "爱给网-2d素材库-免费下载.txt", "爱给网-虚幻(UE)-免费下载.txt", "爱给网-源码-免费下载.txt","必看!UE4资源使用说明.txt","爱给网-3d模型-免费下载.txt","免责声明.txt",
                   "UE4资源安装说明.txt","免责声明【必看】.txt","  UE多个高质量写实风景地貌场景模型_-传奇素材包-素材说明.txt",
                   "UE4库文件使用教程.docx"]

# 代码2静默模式（True=隐藏命令行窗口，False=显示）
silent_mode = True

# 代码2报告类型: "console" / "csv" / "both"
REPORT_TYPE = "console"


# 请在此处填入嵌入式二进制文件的 Base64 字符串
# 注意：这些二进制文件必须正确编码，否则程序无法运行

# 7z 相关二进制文件（代码1需要）


# WinRAR 相关二进制文件（代码1和代码2都需要）


# ===================== 自动检测并安装 tqdm 库（用于代码1） =====================
def ensure_tqdm():
    """检测 tqdm 库，如果缺失则自动安装"""
    try:
        from tqdm import tqdm
        return tqdm
    except ImportError:
        print("检测到缺少 tqdm 库，正在自动安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
            print("安装成功！正在重新导入...")
            from tqdm import tqdm
            return tqdm
        except Exception as e:
            print(f"自动安装失败: {e}")
            print("请手动运行以下命令安装：pip install tqdm")
            print("\n按任意键退出...")
            if sys.platform.startswith('win'):
                import msvcrt
                msvcrt.getch()
            else:
                input()
            sys.exit(1)

tqdm = ensure_tqdm()

# ===================== 代码1：便携式压缩工具管理器 =====================
class PortableCompressionTools:
    """
    便携式压缩工具管理器
    负责从嵌入式二进制数据中提取和管理7z和WinRAR工具
    """
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="compression_tools_")
        self.extracted_files = {}
        self.is_initialized = False
        
    def extract_binary(self, binary_data, filename):
        if not binary_data:
            return None
        file_path = os.path.join(self.temp_dir, filename)
        try:
            clean_base64 = binary_data.replace('\n', '').replace(' ', '')
            file_data = base64.b64decode(clean_base64)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            return file_path
        except Exception as e:
            print(f"提取文件 {filename} 时出错: {str(e)}")
            return None
    
    def initialize_tools(self):
        if self.is_initialized:
            return True
        print("初始化便携式压缩工具...")
        try:
            sevenzip_files = [
                ("7z.exe", BIN_7Z),
                ("7z.dll", BIN_7Z_DLL),
                ("7z.sfx", BIN_7Z_SFX),
                ("7zCon.sfx", BIN_7ZCON_SFX),
            ]
            winrar_files = [
                ("WinRAR.exe", BIN_WINRAR),
                ("Rar.exe", BIN_RAR),
                ("UnRAR.exe", BIN_UNRAR),
                ("RarExt.dll", BIN_RAREXT_DLL),
            ]
            print("提取7z工具...")
            for filename, binary_data in sevenzip_files:
                if binary_data:
                    file_path = self.extract_binary(binary_data, filename)
                    if file_path:
                        self.extracted_files[filename] = file_path
                        print(f"  ✓ {filename}")
                    else:
                        print(f"  ✗ {filename} (提取失败)")
            print("提取WinRAR工具...")
            for filename, binary_data in winrar_files:
                if binary_data:
                    file_path = self.extract_binary(binary_data, filename)
                    if file_path:
                        self.extracted_files[filename] = file_path
                        print(f"  ✓ {filename}")
                    else:
                        print(f"  ✗ {filename} (提取失败)")
            required_7z = ["7z.exe", "7z.dll"]
            required_winrar = ["WinRAR.exe", "RarExt.dll"]
            for req_file in required_7z:
                if req_file not in self.extracted_files:
                    print(f"错误: 缺少必要7z文件 - {req_file}")
                    return False
            for req_file in required_winrar:
                if req_file not in self.extracted_files:
                    print(f"错误: 缺少必要WinRAR文件 - {req_file}")
                    return False
            self.is_initialized = True
            print("✓ 工具初始化完成")
            return True
        except Exception as e:
            print(f"✗ 工具初始化失败: {str(e)}")
            return False
    
    def get_7z_path(self):
        return self.extracted_files.get("7z.exe")
    
    def get_winrar_path(self):
        return self.extracted_files.get("WinRAR.exe")
    
    def get_rar_path(self):
        return self.extracted_files.get("Rar.exe")
    
    def cleanup(self):
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                print(f"已清理临时目录: {self.temp_dir}")
        except Exception as e:
            print(f"清理临时文件时出错: {str(e)}")

# ===================== 代码1辅助函数 =====================
def create_silent_process_config():
    startupinfo = None
    creationflags = 0
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        creationflags = subprocess.CREATE_NO_WINDOW
    return startupinfo, creationflags

def convert_zip_to_rar(zip_file, rar_file, tools_manager):
    startupinfo, creationflags = create_silent_process_config()
    temp_dir = tempfile.mkdtemp()
    winrar_path = tools_manager.get_winrar_path()
    if not winrar_path:
        return False, "WinRAR工具未找到"
    try:
        subprocess.run(
            [winrar_path, "x", "-ibck", "-idq", "-o+", zip_file, f"{temp_dir}\\"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            startupinfo=startupinfo,
            creationflags=creationflags
        )
        subprocess.run(
            [winrar_path, "a", "-idq", "-ibck", "-ep1", "-r", "-o+", rar_file, f"{temp_dir}\\*.*"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            startupinfo=startupinfo,
            creationflags=creationflags
        )
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, f"子进程执行错误: {e.returncode}"
    except Exception as e:
        return False, f"意外错误: {str(e)}"
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def convert_7z_to_rar(seven_zip_file, rar_file, tools_manager):
    startupinfo, creationflags = create_silent_process_config()
    sevenzip_path = tools_manager.get_7z_path()
    winrar_path = tools_manager.get_winrar_path()
    if not sevenzip_path:
        return False, "7z工具未找到"
    if not winrar_path:
        return False, "WinRAR工具未找到"
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.run(
                [sevenzip_path, "x", f"-o{temp_dir}", seven_zip_file, "-y", "-spd"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            subprocess.run(
                [winrar_path, "a", "-idq", "-ibck", "-r", "-o+", "-ep1", rar_file, os.path.join(temp_dir, "*")],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            return True, ""
    except subprocess.CalledProcessError as e:
        return False, f"子进程执行错误: {str(e)}"
    except Exception as e:
        return False, f"意外错误: {str(e)}"

def process_file(file_path, tools_manager):
    """处理单个文件，转换成功后删除原始文件，返回 (成功?, 消息, 生成的rar路径或None)"""
    if not os.path.exists(file_path):
        return False, f"文件不存在: {file_path}", None
    ext = os.path.splitext(file_path)[1].lower()
    rar_path = os.path.splitext(file_path)[0] + '.rar'
    if os.path.exists(rar_path):
        return True, f"跳过: RAR文件已存在 - {os.path.basename(rar_path)}", rar_path
    try:
        if ext == '.zip':
            success, message = convert_zip_to_rar(file_path, rar_path, tools_manager)
        elif ext == '.7z':
            success, message = convert_7z_to_rar(file_path, rar_path, tools_manager)
        else:
            return False, f"跳过: 不支持的文件类型 - {os.path.basename(file_path)}", None
        if not success:
            return False, f"转换失败: {os.path.basename(file_path)} - {message}", None
        result_msg = f"成功: {os.path.basename(file_path)} -> {os.path.basename(rar_path)}"
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                result_msg += " (原始文件已删除)"
            else:
                result_msg += " (原始文件已被删除)"
        except Exception as e:
            result_msg += f" (警告: 无法删除原始文件 - {str(e)})"
        return True, result_msg, rar_path
    except Exception as e:
        return False, f"异常: 处理文件时出错 - {os.path.basename(file_path)} - {str(e)}", None

def process_directory_for_convert(directory):
    """返回目录中的所有ZIP和7Z文件列表"""
    zip_files = []
    try:
        if not os.path.exists(directory):
            print(f"错误: 目录不存在 - {directory}")
            return zip_files
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.zip', '.7z')):
                    full_path = os.path.join(root, file)
                    if os.path.isfile(full_path):
                        zip_files.append(full_path)
        return zip_files
    except Exception as e:
        print(f"异常: 处理目录时出错 - {directory} - {str(e)}")
        return zip_files

# ===================== 代码2：便携式RAR工具管理器及冗余删除功能 =====================
ResultItem = namedtuple('ResultItem', ['rar_path', 'success', 'deleted_count', 'error_msg', 'patterns'])

class PortableRARTools:
    """便携式RAR工具管理器（代码2）"""
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="rar_tools_")
        self.extracted_files = {}
        self.is_initialized = False
        self.rar_exe_path = None

    def extract_binary(self, binary_data, filename):
        if not binary_data:
            return None
        file_path = os.path.join(self.temp_dir, filename)
        try:
            clean_base64 = binary_data.replace('\n', '').replace(' ', '')
            file_data = base64.b64decode(clean_base64)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            return file_path
        except Exception as e:
            print(f"提取文件 {filename} 时出错: {str(e)}")
            return None

    def initialize_tools(self):
        if self.is_initialized:
            return True
        print("初始化便携式RAR工具...")
        try:
            rar_files = [
                ("Rar.exe", BIN_RAR),
                ("UnRAR.exe", BIN_UNRAR),
                ("RarExt.dll", BIN_RAREXT_DLL),
            ]
            for filename, binary_data in rar_files:
                if binary_data:
                    file_path = self.extract_binary(binary_data, filename)
                    if file_path:
                        self.extracted_files[filename] = file_path
                        print(f"  ✓ {filename}")
                    else:
                        print(f"  ✗ {filename} (提取失败)")
            self.rar_exe_path = self.extracted_files.get("Rar.exe")
            if not self.rar_exe_path:
                print("错误: 无法提取Rar.exe")
                return False
            if "RarExt.dll" not in self.extracted_files:
                print("警告: RarExt.dll未找到，某些功能可能受限")
            self.is_initialized = True
            print("✓ RAR工具初始化完成")
            return True
        except Exception as e:
            print(f"✗ RAR工具初始化失败: {str(e)}")
            return False

    def get_rar_exe_path(self):
        return self.rar_exe_path

    def cleanup(self):
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                print(f"已清理临时目录: {self.temp_dir}")
        except Exception as e:
            print(f"清理临时文件时出错: {str(e)}")

def get_silent_args():
    if os.name == 'nt' and silent_mode:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        return {'startupinfo': si}
    return {}

def filter_parent_entries(entries):
    normalized_dict = {}
    for entry in entries:
        normalized = entry.replace('\\', '/').strip('/')
        normalized_dict[normalized] = entry
    normalized_set = set(normalized_dict.keys())
    filtered = []
    for norm_path in normalized_set:
        if not norm_path:
            continue
        parts = norm_path.split('/')
        parent_paths = ['/'.join(parts[:i+1]) for i in range(len(parts)-1)]
        if not any(parent in normalized_set for parent in parent_paths):
            filtered.append(normalized_dict[norm_path])
    return filtered

def get_entries_to_delete(rar_path, rar_exe_path):
    try:
        cmd = [rar_exe_path, 'lb', rar_path]

        # 使用系统默认编码（Windows下通常是gbk）
        import sys
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding=sys.getfilesystemencoding(), errors='replace', **get_silent_args())
        
        if result.stdout is None:
            return []
    except subprocess.CalledProcessError as e:
        print(f"无法列出压缩包内容: {os.path.basename(rar_path)} - {str(e)}")
        return []
    raw_entries = result.stdout.splitlines() if result.stdout else []
    candidates = []
    for entry in raw_entries:
        normalized = entry.replace('\\', '/').strip('/')
        parts = [p for p in normalized.split('/') if p]
        if any(part in delete_patterns for part in parts):
            candidates.append(entry)
    unique_entries = list(set(candidates))

    # 新增：规范化路径，去除前导反斜杠或盘符
    normalized_entries = []
    for entry in unique_entries:
        # 去除前导的 \ 或 / 或盘符（如 C:\）
        entry_clean = entry.lstrip('\\').lstrip('/')
        if entry_clean and ':' in entry_clean and len(entry_clean) > 1 and entry_clean[1] == ':':
            # 去除盘符前缀，如 "C:\Folder" -> "Folder"
            entry_clean = entry_clean[2:].lstrip('\\').lstrip('/')
        normalized_entries.append(entry_clean)

    return filter_parent_entries(normalized_entries)

def process_rar(rar_path, rar_exe_path):
    entries = get_entries_to_delete(rar_path, rar_exe_path)
    if not entries:
        return 0, set()
    
    # 计算匹配的模式
    matched = set()
    for entry in entries:
        parts = entry.replace('\\', '/').split('/')
        matched.update(set(parts) & set(delete_patterns))
    
    try:
        # 使用列表文件批量删除
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            list_file = f.name
            for entry in entries:
                f.write(entry + '\n')
        cmd = [rar_exe_path, 'd', '-idq', rar_path, '@' + list_file]
        result = subprocess.run(cmd, capture_output=True, text=True,
                                encoding=sys.getfilesystemencoding(), errors='replace',
                                **get_silent_args())
        # 删除临时列表文件
        os.unlink(list_file)
        # 返回码 0 表示成功，10 表示未找到文件（可能条目已经被删），我们也视为成功
        if result.returncode not in (0, 10):
            raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
        return len(entries), matched
    except subprocess.CalledProcessError as e:
        error_msg = f"RAR命令执行失败: {str(e)}"
        if "Cannot find" in str(e):
            error_msg += "（可能因父目录已被删除）"
        raise Exception(error_msg)
    except Exception as e:
        raise Exception(f"批量删除失败: {str(e)}")

def generate_console_report(results):
    print("\n" + "=" * 50)
    print("处理结果汇总:")
    for res in results:
        status = "[失败]" if not res.success else "[跳过]" if not res.deleted_count else "[成功]"
        base_info = f"{status} {os.path.basename(res.rar_path)}"
        if not res.success:
            print(f"{base_info} - 错误: {res.error_msg}")
        elif res.deleted_count:
            print(f"{base_info.ljust(40)} 删除: {res.deleted_count}项 | 匹配模式: {', '.join(res.patterns)}")
        else:
            print(base_info)
    print("=" * 50)

def generate_csv_report(results, base_dir):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_name = f"RAR清理报告_{timestamp}.csv"
    csv_path = os.path.join(base_dir, csv_name)
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["压缩包名称", "相对路径", "绝对路径", "处理状态", "删除数量", "匹配模式", "错误信息"])
            for res in results:
                try:
                    relative_path = os.path.relpath(res.rar_path, base_dir)
                except ValueError:
                    relative_path = res.rar_path
                status = "成功" if res.success else "失败"
                patterns = ', '.join(res.patterns) if res.patterns else ""
                error = res.error_msg if res.error_msg else ""
                writer.writerow([
                    os.path.basename(res.rar_path),
                    relative_path,
                    res.rar_path,
                    status,
                    res.deleted_count,
                    patterns,
                    error
                ])
        print(f"CSV报告已生成: {csv_path}")
        return csv_path
    except Exception as e:
        print(f"生成CSV报告失败: {str(e)}")
        return None

def collect_rar_files(paths):
    """从路径列表收集所有RAR文件（用于代码2）"""
    rar_files = []
    for path_str in paths:
        path = Path(path_str)
        if not path.exists():
            print(f"警告: 路径不存在: {path}")
            continue
        if path.is_file():
            if path.suffix.lower() == '.rar':
                rar_files.append(str(path))
                print(f"添加RAR文件: {path.name}")
            else:
                print(f"跳过非RAR文件: {path.name}")
        elif path.is_dir():
            try:
                dir_rar_count = 0
                for rar_path in path.rglob('*.rar'):
                    rar_files.append(str(rar_path))
                    dir_rar_count += 1
                print(f"在文件夹 '{path.name}' 中发现 {dir_rar_count} 个RAR文件")
            except Exception as e:
                print(f"扫描文件夹失败 '{path}': {str(e)}")
    return rar_files

def wait_for_exit():
    if sys.platform.startswith('win'):
        print("\n程序执行完毕，按任意键退出...")
        import msvcrt
        msvcrt.getch()
    else:
        input("\n程序执行完毕，按回车键退出...")

def get_base_directory(paths):
    if not paths:
        return os.getcwd()
    first_path = Path(paths[0])
    if first_path.is_file():
        return str(first_path.parent)
    else:
        return str(first_path)

# ===================== 简易进度条（代码2使用） =====================
class SimpleProgressBar:
    def __init__(self, iterable=None, desc="", total=None, unit="it"):
        self.desc = desc
        self.iterable = iterable
        self.total = total if total is not None else (len(iterable) if iterable else None)
        self.unit = unit
        self.start_time = time.time()
        self.current = 0
        self._print_description()
    def _print_description(self):
        if self.total:
            print(f"{self.desc} ({self.total} {self.unit})...", end="", flush=True)
        else:
            print(f"{self.desc}...", end="", flush=True)
    def __iter__(self):
        self.current = 0
        for item in self.iterable:
            yield item
            self.current += 1
            self.update(1)
    def update(self, n=1):
        if self.total and self.current % max(1, self.total // 50) == 0:
            print(".", end="", flush=True)
    def set_postfix(self, **kwargs):
        pass
    def close(self):
        elapsed = time.time() - self.start_time
        print(f" 完成 [{self.current}/{self.total if self.total else '?'}]，耗时 {elapsed:.2f}s")
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# ===================== 融合主程序 =====================
def main():
    # 第一阶段：初始化代码1的工具
    tools_compress = PortableCompressionTools()
    if not tools_compress.initialize_tools():
        print("错误: 无法初始化压缩工具（代码1）")
        print("请确保二进制变量已正确填充")
        wait_for_exit()
        return

    # 解析命令行参数（支持拖放）
    parser = argparse.ArgumentParser(description='ZIP/7Z转RAR + RAR冗余清理工具')
    parser.add_argument('paths', nargs='*', help='要处理的文件或文件夹路径')
    args = parser.parse_args()

    if not args.paths:
        print("提示: 您可以直接将文件或文件夹拖放到此程序上，或手动输入路径")
        input_path = input("请拖放文件或文件夹到此处，或直接输入路径: ").strip().strip('"')
        if not input_path:
            print("未提供路径，程序退出")
            tools_compress.cleanup()
            wait_for_exit()
            return
        target_paths = [input_path]
    else:
        target_paths = args.paths

    # 收集所有需要处理的原始路径
    all_input_paths = []
    for path_str in target_paths:
        if os.path.exists(path_str):
            all_input_paths.append(path_str)
        else:
            print(f"警告: 路径不存在 - {path_str}")

    # ========== 步骤1：转换ZIP/7Z为RAR，并收集所有RAR文件 ==========
    print("\n" + "="*60)
    print("步骤1: 转换ZIP/7Z文件为RAR格式")
    print("="*60)

    # 收集所有待转换的文件（ZIP/7Z）
    files_to_convert = []
    for path in all_input_paths:
        if os.path.isfile(path):
            if path.lower().endswith(('.zip', '.7z')):
                files_to_convert.append(path)
            # 注意：RAR文件不在此步骤处理，留到步骤2
        elif os.path.isdir(path):
            dir_files = process_directory_for_convert(path)
            files_to_convert.extend(dir_files)

    # 去重
    files_to_convert = list(set(files_to_convert))

    # 存储转换后生成的RAR路径以及原本就存在的RAR路径
    all_rar_files = set()

    if files_to_convert:
        print(f"找到 {len(files_to_convert)} 个需要转换的文件")
        success_count = 0
        with tqdm(files_to_convert, desc="转换进度", unit="file", colour="blue") as pbar:
            for file_path in pbar:
                base_name = os.path.basename(file_path)
                pbar.set_postfix(file=base_name[:20])
                success, message, generated_rar = process_file(file_path, tools_compress)
                if success:
                    if "成功" in message:
                        success_count += 1
                    if generated_rar and os.path.exists(generated_rar):
                        all_rar_files.add(generated_rar)
                    pbar.write(f"[✓] {message}")
                else:
                    pbar.write(f"[✕] {message}")
        print(f"\n转换完成！成功转换 {success_count}/{len(files_to_convert)} 个文件")
    else:
        print("未发现需要转换的ZIP或7Z文件")

    # 收集输入路径中原本的RAR文件（不经过转换）
    original_rar_paths = []
    for path in all_input_paths:
        if os.path.isfile(path) and path.lower().endswith('.rar'):
            original_rar_paths.append(path)
        elif os.path.isdir(path):
            for rar_path in Path(path).rglob('*.rar'):
                original_rar_paths.append(str(rar_path))
    all_rar_files.update(original_rar_paths)

    # 去重
    all_rar_files = list(set(all_rar_files))

    if not all_rar_files:
        print("\n未找到任何RAR文件（包括转换生成的），无需执行步骤2。")
        tools_compress.cleanup()
        wait_for_exit()
        return

    print(f"\n步骤1完成，共收集到 {len(all_rar_files)} 个RAR文件，准备执行冗余文件删除。")

    # ========== 步骤2：对收集到的所有RAR文件执行冗余删除 ==========
    print("\n" + "="*60)
    print("步骤2: RAR冗余文件删除")
    print("="*60)

    # 初始化代码2的工具
    tools_rar = PortableRARTools()
    if not tools_rar.initialize_tools():
        print("错误: 无法初始化RAR工具（代码2）")
        print("请确保二进制变量已正确填充")
        tools_compress.cleanup()
        wait_for_exit()
        return

    rar_exe_path = tools_rar.get_rar_exe_path()
    if not rar_exe_path:
        print("错误: 无法获取RAR工具路径")
        tools_compress.cleanup()
        tools_rar.cleanup()
        wait_for_exit()
        return

    print(f"使用RAR工具: {rar_exe_path}")

    # 确定基础目录（用于CSV报告）
    base_dir = get_base_directory(target_paths)

    print("="*60)
    print("开始扫描RAR文件...")
    print("="*60)

    # 显示所有将要处理的RAR文件
    print(f"\n总共发现待处理RAR文件: {len(all_rar_files)}个")
    print("文件列表:")
    for i, rar_file in enumerate(all_rar_files, 1):
        print(f"  {i:2d}. {rar_file}")

    print(f"\n按回车键开始处理这 {len(all_rar_files)} 个文件，按其他任意键取消...")
    response = input()
    if response != "":
        print("用户取消操作")
        tools_compress.cleanup()
        tools_rar.cleanup()
        wait_for_exit()
        return

    results = []
    print("\n开始处理RAR文件...")
    with SimpleProgressBar(all_rar_files, desc="处理压缩包", unit="file") as pbar:
        for rar_path in pbar:
            try:
                if not os.path.isfile(rar_path):
                    raise Exception("文件不存在或已被删除")
                deleted_count, patterns = process_rar(rar_path, rar_exe_path)
                success = True
                error_msg = None
                if deleted_count > 0:
                    status_str = f"删除{deleted_count}项".ljust(12)
                    print(f"\n[✓] {os.path.basename(rar_path)[:30].ljust(32)} {status_str} 匹配模式: {', '.join(patterns)}")
                else:
                    print(f"\n[○] {os.path.basename(rar_path)} 无需处理")
            except Exception as e:
                success = False
                error_msg = str(e)
                deleted_count = 0
                patterns = set()
                print(f"\n[×] 处理失败: {os.path.basename(rar_path)} - {error_msg}")
            results.append(ResultItem(
                rar_path=rar_path,
                success=success,
                deleted_count=deleted_count,
                error_msg=error_msg,
                patterns=patterns
            ))

    # 生成报告
    if REPORT_TYPE in ("console", "both"):
        generate_console_report(results)
    if REPORT_TYPE in ("csv", "both"):
        csv_path = generate_csv_report(results, base_dir)
        if csv_path:
            print(f"\nCSV报告路径: {os.path.abspath(csv_path)}")

    # 显示摘要
    print("\n" + "="*60)
    print("处理结果摘要:")
    print("="*60)
    success_count = sum(1 for r in results if r.success and r.deleted_count > 0)
    skipped_count = sum(1 for r in results if r.success and r.deleted_count == 0)
    failed_count = sum(1 for r in results if not r.success)
    total_deleted = sum(r.deleted_count for r in results)
    print(f"成功处理并删除文件: {success_count} 个")
    print(f"无需处理: {skipped_count} 个")
    print(f"处理失败: {failed_count} 个")
    print(f"总共删除条目: {total_deleted} 个")

    # 清理临时文件
    tools_compress.cleanup()
    tools_rar.cleanup()
    wait_for_exit()

if __name__ == "__main__":
    main()