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

# A dict stored addresses and usernames of all connecting clients
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
    # delete user info if exists.
    if name in user:
        del user[name]
    for a in user.values():
        sock.sendto(content.encode(), a)


def handle(sock):
    while True:
        request, addr = sock.recvfrom(1024)
        info = request.decode().split(" ", 1)
        request = info[0]
        content = info[1]
        if request == "LOGIN":
            join_group(sock, addr, content)
        elif request == "CHAT":
            chat(sock, addr, content)
        elif request == "EXIT":
            exit_group(sock, content)


# Entry function
def main():
    sock = socket(type=SOCK_DGRAM)
    sock.bind(ADDR)
    # Create a process to receive requests from clients.
    p = Process(target=handle, args=(sock,), daemon=True)
    p.start()
    # To create a group notice anytime you want.
    while True:
        admin_notice = input("Group Notice:")
        # Send group notice by child process.
        notice = "CHAT " + "Group Notice:" + admin_notice
        sock.sendto(notice.encode(), ADDR)


if __name__ == '__main__':
    main()
