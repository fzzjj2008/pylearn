# -*- coding: utf-8 -*-
'''
@Date: 2020-03-04 22:48:02
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-04 23:42:21
'''
"""
UDP socket server
地址：127.0.0.1
端口：8888
"""
from socket import socket, AF_INET, SOCK_DGRAM

server = socket(AF_INET, SOCK_DGRAM)
server.bind(('127.0.0.1', 8888))
print('服务器启动')
while True:
    data, addr = server.recvfrom(1024)
    print(data, addr)
    reply = '服务端收到：%s' % data
    server.sendto(reply.encode('utf-8'), addr)