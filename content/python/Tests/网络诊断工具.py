# network_diagnose.py
import socket
import subprocess
import platform

def diagnose_connection(host, port):
    print("=== 网络连接诊断 ===")
    print(f"目标: {host}:{port}")
    
    # 1. 检查主机是否可达
    print("\n1. 检查主机可达性...")
    try:
        # 根据操作系统选择ping命令
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "3", host]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ 主机可达")
        else:
            print("✗ 主机不可达")
            print("请检查IP地址是否正确")
            return False
    except Exception as e:
        print(f"Ping测试失败: {e}")
    
    # 2. 检查端口是否开放
    print("\n2. 检查端口状态...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"✓ 端口 {port} 开放")
        else:
            print(f"✗ 端口 {port} 关闭 (错误代码: {result})")
            print("可能的原因:")
            if result == 10061:
                print("  - 连接被拒绝，被控端可能未运行")
            elif result == 10060:
                print("  - 连接超时")
            elif result == 10035:
                print("  - 非阻塞操作无法立即完成")
            else:
                print(f"  - 系统错误代码: {result}")
            return False
    finally:
        sock.close()
    
    # 3. 测试实际连接
    print("\n3. 测试实际连接...")
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(5)
        test_socket.connect((host, port))
        test_socket.close()
        print("✓ 连接测试成功")
        return True
    except socket.timeout:
        print("✗ 连接超时")
        return False
    except ConnectionRefusedError:
        print("✗ 连接被拒绝")
        return False
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False

def check_firewall():
    print("\n4. 防火墙检查...")
    system = platform.system().lower()
    
    if system == "windows":
        try:
            # 检查Windows防火墙状态
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"], 
                capture_output=True, 
                text=True
            )
            if "状态                                  开" in result.stdout:
                print("⚠ Windows防火墙已开启，可能阻止连接")
                print("建议: 为Python添加防火墙例外")
            else:
                print("✓ Windows防火墙已关闭")
        except:
            print("无法检查防火墙状态")
    else:
        print("非Windows系统，请手动检查防火墙设置")

if __name__ == "__main__":
    host = input("请输入被控端IP地址: ").strip()
    port = int(input("请输入端口号 (默认8888): ") or "8888")
    
    diagnose_connection(host, port)
    check_firewall()
    
    print("\n=== 诊断完成 ===")
    input("按回车键退出...")