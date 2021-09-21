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
PORT = 7500
ADDR = (HOST, PORT)



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
    # Create a process to receive messages
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
