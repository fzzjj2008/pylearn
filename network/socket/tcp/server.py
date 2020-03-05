# -*- coding: utf-8 -*-
'''
@Date: 2020-03-04 22:47:43
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-04 23:36:10
'''

"""
TCP socket server
地址：127.0.0.1
端口：8888
监听数：5
"""
from socket import socket, AF_INET, SOCK_STREAM

server = socket(AF_INET, SOCK_STREAM)
server.bind(('127.0.0.1', 8888))
server.listen(5)
while True:
    print('服务器启动，监听客户端')
    conn, addr = server.accept()
    print('客户端：', addr)
    while True:
        try:
            data = conn.recv(1024)
        except Exception:
            print('断开客户端', addr)
            break
        print('客户端发送：%s' % data.decode('utf-8'))
        if not data:
            break
        msg = '服务端收到消息：%s' % data.decode('utf-8')
        conn.send(msg.encode('utf-8'))
    conn.close()
server.close()
