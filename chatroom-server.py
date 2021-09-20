"""
Author : Jacob
Email : jacob7154@qq.com
Env : python3
Time : 2021-8-15
GroupChat Project
"""

from socket import *
from multiprocessing import Process

# Address of Server
HOST = "0.0.0.0"
PORT = 7154
ADDR = (HOST, PORT)


user = {}


def join_group(sock, address, name):

    if name in user:
        sock.sendto(b"FAIL", address)
        return
    # Inform user who has joined in group chat successfully.
    sock.sendto(b"OK", address)
    # Inform others that someone has joined in.
    msg = f"Welcome {name}!"
    for person in user:
        sock.sendto(msg.encode(), user[person])
    # Register client-address of present user in dict_users
    user[name] = address


def chat(sock, addr, message):
    name = message.split(":", 1)[0]
    for u, a in user.items():
        if u == name:
            continue
        sock.sendto(message.encode(), a)


def exit_group(sock, content):
    name = content.split(" ", 1)[0]
    # 确保用户在列表才能删除
    if name in user:
        del user[name]
    for a in user.values():
        sock.sendto(content.encode(), a)


def handle(sock):
    # 一处总体接收各种请求，分情况解析讨论
    while True:
        request, addr = sock.recvfrom(1024)
        # print(request)
        info = request.decode().split(" ", 1)
        request = info[0]
        content = info[1]
        # 分情况讨论
        if request == "LOGIN":
            join_group(sock, addr, content)
            # print(DICT_USER)
        elif request == "CHAT":
            chat(sock, addr, content)
        elif request == "EXIT":
            exit_group(sock, content)


# 先写入口　搭建框架
def main():
    # 创建UDP网络模型
    sock = socket(type=SOCK_DGRAM)
    sock.bind(ADDR)
    # 创建进程
    p = Process(target=handle, args=(sock,), daemon=True)
    p.start()
    # 创建管理员消息
    while True:
        admin_notice = input("Group Notice:")
        # 通过进程间通信将管理员消息传入子进程
        notice = "CHAT " + "Group Notice:" + admin_notice
        sock.sendto(notice.encode(), ADDR)      # 注意这里是发给服务端


if __name__ == '__main__':
    main()
