import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)
result = s.connect_ex(('192.168.1.198', 8888))
if result == 0:
    print("端口可连接")
else:
    print(f"端口不可连接，错误代码: {result}")
s.close()