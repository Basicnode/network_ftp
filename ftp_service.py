# -*- coding: utf-8 -*-
# @Author: zt
# @Time: 2023/9/20 18:05

# 导入所需模块
import os
import socket
from configure import config


def service():
    # 定义服务器主机和端口
    HOST = config.get(section='section', key='host')
    PORT = int(config.get(section='section', key='port'))

    # 创建服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    while True:
        # 等待客户端连接
        print('等待客户端连接...')
        client_socket, addr = server_socket.accept()
        print('客户端已连接，地址：', addr)

        # 接收客户端发送的下载/上传编号
        user_input = client_socket.recv(1024).decode('utf-8')
        print('user_input: ', user_input)
        if user_input == '1':
            # 接收客户端发送的文件名
            filename = client_socket.recv(1024).decode('utf-8')
            print('接收文件名：', filename)

            # 获取当前目录
            current_dir = os.getcwd()
            # 拼接文件路径
            fp = os.path.join(current_dir, filename)
            # 判断文件是否存在
            if os.path.exists(fp):
                print('文件存在')
                # 打开文件并读取文件内容
                file = open(filename, 'rb')
                data = file.read()
            else:
                print('文件不存在')
                client_socket.sendall('文件不存在'.encode())
                continue

            # 发送文件内容给客户端
            client_socket.sendall(data)
            print('文件发送成功')

            # 关闭连接
            client_socket.close()
            print('连接已关闭')
        elif user_input == '2':
            # 接收客户端发送的文件
            filename = client_socket.recv(1024)
            print('文件名：', filename)
            # 保存文件
            try:
                with open(filename, 'wb') as file:
                    file.write(filename)
                    client_socket.send('文件上传成功'.encode())
            except Exception as e:
                print('文件保存异常：'.encode(), e)
                client_socket.send('文件保存异常'.encode())
        else:
            client_socket.close()


if __name__ == '__main__':
    service()

