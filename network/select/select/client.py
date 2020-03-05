# -*- coding: utf-8 -*-
'''
@Date: 2020-03-05 00:13:55
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-05 23:56:53
'''

from socket import socket, AF_INET, SOCK_STREAM

client = socket(AF_INET, SOCK_STREAM)
client.connect(('localhost', 8090))
while True:
    data = input('>>').strip()
    if not data:
        break
    client.send(data.encode('utf-8'))
    print(client.recv(1024))
client.close()
