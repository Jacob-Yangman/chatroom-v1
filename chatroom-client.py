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
    服务端做什么？——保存用户信息接收入群消息，发布入群消息，发公告
    客户端做什么？——输入姓名、发消息
"""

from socket import *
from multiprocessing import Process

# Address of Server
HOST = "0.0.0.0"
PORT = 7154
ADDR = (HOST, PORT)


# 客户端框架　　UDP模型

def login(sock):
    while True:
        name = input("Please input your name >>> ")
        msg = "LOGIN " + name
        sock.sendto(msg.encode(), ADDR)
        reply, addr = sock.recvfrom(1024)
        if reply == b"OK":
            print("You have joined chatroom successfully!")
            return name
        else:
            print("This name has exists!")


def send_msg(sock, name):
    while True:
        try:
            message = input("")
        except KeyboardInterrupt:
            message = "quit"

        if message == "quit":
            msg = "EXIT " + name + " has quit group chat!"
            sock.sendto(msg.encode(), ADDR)
            break

        whole_msg = f"{name}:{message}"
        sock.sendto(b"CHAT " + whole_msg.encode(), ADDR)



def recv_msg(sock):
    while True:
        information, addr = sock.recvfrom(1024)
        print("\t\t\t", information.decode())


def chat(sock, name):
    info_process = Process(target=recv_msg, args=(sock,), daemon=True)
    info_process.start()

    send_msg(sock, name)



# Entrance Function
def main():
    sock = socket(type=SOCK_DGRAM)
    # Enter the chatroom
    name = login(sock)
    # Circularly send and receive message
    chat(sock, name)

    sock.close()


if __name__ == '__main__':
    main()
