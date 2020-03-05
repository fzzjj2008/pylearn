# -*- coding: utf-8 -*-
'''
@Date: 2020-03-04 22:48:08
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-04 23:45:24
'''
"""
UDP socket client
地址：127.0.0.1
端口：8888
"""

from socket import socket, AF_INET, SOCK_DGRAM

ADDR = (('127.0.0.1', 8888))
client = socket(AF_INET, SOCK_DGRAM)

for data in [b'Michael', b'Tracy']:
    client.sendto(data, ADDR)
    print(client.recv(1024).decode('utf-8'))
client.close()