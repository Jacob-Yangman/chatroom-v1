"""
Author : Jacob
Email : jacob7154@qq.com
Env : python3
Time : 2021-8-15
GroupChat Project
"""

"""
**群聊聊天室 **

> 功能 ： 类似qq群功能

> 【1】 有人进入聊天室需要输入姓名，姓名不能重复
> 【2】 有人进入聊天室时，其他人会收到通知：**Lucy 进入了聊天室**
> 【3】 一个人发消息，其他人会收到：   **Lucy ： 一起出去玩啊。**
> 【4】 有人退出聊天室，则其他人也会收到通知 :  **Lucy 退出了聊天室**
> 【5】 扩展功能：服务器可以向所有用户发送公告:    **管理员消息： 大家好，欢迎进入聊天室。**
"""

"""
    需求分析：要给其他人发消息——消息队列？服务端？客户端
    服务端做什么？——保存用户信息　接收入群消息，发布入群消息，发公告
    客户端做什么？——输入姓名、发消息
"""


from socket import *
from multiprocessing import Process

# 服务器地址
HOST = "0.0.0.0"
PORT = 7154
ADDR = (HOST, PORT)

# 用户信息字典
user = {}


def join_group(sock, address, name):
    # 判断用户名是否已存在
    if name in user:
        sock.sendto(b"FAIL", address)
        return
    # 通知当前用户入群成功
    sock.sendto(b"OK", address)
    # 向其他人发送当前用户入群消息
    msg = f"Welcome {name}!"
    for person in user:
        sock.sendto(msg.encode(), user[person])
    # 在用户信息字典中添加当前用户地址
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
    # print(user)       # 测试
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
