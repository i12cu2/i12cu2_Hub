# fix_firewall.py
import subprocess
import sys
import os

def add_firewall_exception(port, name="Python Remote Control"):
    """为指定端口添加Windows防火墙例外"""
    try:
        # 检查是否以管理员权限运行
        if not is_admin():
            print("请以管理员权限运行此脚本!")
            return False
        
        # 添加入站规则
        commands = [
            f'netsh advfirewall firewall add rule name="{name} TCP" dir=in action=allow protocol=TCP localport={port}',
            f'netsh advfirewall firewall add rule name="{name} UDP" dir=in action=allow protocol=UDP localport={port}'
        ]
        
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"✓ {cmd}")
            else:
                print(f"✗ 执行失败: {cmd}")
                print(f"错误: {result.stderr}")
                return False
        
        print(f"\n✓ 已为端口 {port} 添加防火墙例外")
        return True
        
    except Exception as e:
        print(f"添加防火墙例外失败: {e}")
        return False

def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()

def remove_firewall_exception(name="Python Remote Control"):
    """移除防火墙例外"""
    try:
        if not is_admin():
            print("请以管理员权限运行此脚本!")
            return False
        
        commands = [
            f'netsh advfirewall firewall delete rule name="{name} TCP"',
            f'netsh advfirewall firewall delete rule name="{name} UDP"'
        ]
        
        for cmd in commands:
            subprocess.run(cmd, capture_output=True, shell=True)
        
        print("✓ 已移除防火墙例外")
        return True
        
    except Exception as e:
        print(f"移除防火墙例外失败: {e}")
        return False

if __name__ == "__main__":
    print("=== Windows防火墙配置工具 ===")
    print("1. 添加防火墙例外")
    print("2. 移除防火墙例外")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        port = input("请输入端口号 (默认8888): ").strip() or "8888"
        add_firewall_exception(port)
    elif choice == "2":
        remove_firewall_exception()
    else:
        print("无效选择")
    
    input("按回车键退出...")