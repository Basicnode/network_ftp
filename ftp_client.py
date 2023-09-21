# -*- coding: utf-8 -*-
# @Author: zt
# @Time: 2023/9/20 18:05

# 导入所需模块
import socket
from configure import config


def cli():
    # 定义服务器主机和端口
    HOST = config.get(section='section', key='host')
    PORT = int(config.get(section='section', key='port'))

    # 创建客户端套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接服务器
        client_socket.connect((HOST, PORT))

        user_input = input("请输入选项（1【下载】、2【上传】），输入其他任意字符退出程序：")
        # 将上传/下载编号发送给服务器
        client_socket.sendall(user_input.encode())
        if user_input == '1':
            # 输入要下载的文件名
            filename = input('请输入要下载的文件名：')

            # 将文件名发送给服务器
            client_socket.sendall(filename.encode())

            # 接收服务器发送的文件内容
            data = client_socket.recv(1024)
            if data.decode('utf-8') == '文件不存在':
                print('所需', data.decode('utf-8') + '请输入正确的文件名及后缀信息')
                client_socket.close()
            else:
                # 保存文件路径
                fp = config.get(section='section', key='download_file_path')
                with open(fp + filename, 'wb') as file:
                    file.write(data)
                print('文件下载成功!')

        elif user_input == '2':
            filename = input('请输入要上传的文件名：')
            up_fp_path = config.get(section='section', key='upload_file_path')
            up_file = up_fp_path + filename
            print("up_file", up_file)
            # 向服务器发送文件
            client_socket.sendall(filename.encode())
            msg = client_socket.recv(1024).decode('utf-8')
            print('msg:', msg)

        else:
            client_socket.close()
    except ConnectionRefusedError:
        print('连接被拒绝，请确保服务器已运行')
    finally:
        # 关闭连接
        client_socket.close()


if __name__ == '__main__':
    cli()

