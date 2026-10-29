import socket
import threading

def test_server():
    # 测试服务器是否正常启动
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('0.0.0.0', 8888))
        server_socket.listen(1)
        print("服务器在端口 8888 上正常监听")
        
        # 在另一个线程中测试连接
        def test_connect():
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(('127.0.0.1', 8888))
                client_socket.send(b"test")
                client_socket.close()
                print("本地连接测试成功")
            except Exception as e:
                print(f"本地连接测试失败: {e}")
        
        thread = threading.Thread(target=test_connect)
        thread.daemon = True
        thread.start()
        
        # 接受测试连接
        client, addr = server_socket.accept()
        print(f"接收到测试连接来自: {addr}")
        data = client.recv(1024)
        print(f"接收到数据: {data}")
        client.close()
        
    except Exception as e:
        print(f"服务器启动失败: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    test_server()