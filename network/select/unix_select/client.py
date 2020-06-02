# -*- coding: utf-8 -*-
# Create on: 2020/06/01 14:47:18
# Author   : zhaojiajie

from socket import socket, AF_UNIX, SOCK_STREAM

SOCK_ADDR = "/tmp/unix_sock"

client = socket(AF_UNIX, SOCK_STREAM)
client.connect(SOCK_ADDR)
while True:
    data = client.recv(1024)
    print('收到%s消息：%s' % (client.getpeername(), data.decode('utf-8')))
    if not data:
        print('客户端断开连接')
        break
    else:
        print('发送%s消息：%s' % (client.getpeername(), data))
        client.send(data)
client.close()
