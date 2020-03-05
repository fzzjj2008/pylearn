# -*- coding: utf-8 -*-
'''
@Date: 2020-03-04 22:47:55
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-04 23:18:56
'''

"""
TCP socket server
地址：127.0.0.1
"""
from socket import socket, AF_INET, SOCK_STREAM

client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 8888))
while True:
    data = input('>>').strip()
    if not data:
        break
    client.send(data.encode('utf-8'))
    data = client.recv(1024)
    print(data.decode('utf-8'))
client.close()