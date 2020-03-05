#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Date: 2020-03-06 00:11:45
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-06 01:20:16
'''

import socket
import select
import queue

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置IP地址复用
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('localhost', 8888))
# 监听，并设置最大连接数
serversocket.listen(10)
serversocket.setblocking(False)
print('服务端开始监听')

# 超时时间
timeout = 10
# 创建epoll事件对象，后续要监控的事件添加到其中
epoll = select.epoll()
# 注册服务器监听fd到等待读事件集合
epoll.register(serversocket.fileno(), select.EPOLLIN)
# 保存连接客户端消息的字典，格式为{}
message_queues = {}
# 文件句柄到所对应对象的字典，格式为{句柄：对象}
connections = {}

while True:
    print('等待活动连接......')
    # 轮询注册的事件集合，返回值为[(文件句柄，对应的事件)，(...),....]
    events = epoll.poll(timeout)
    if not events:
        print("epoll超时无活动连接，重新轮询")
        continue
    print("有%d个新事件，开始处理" % (len(events)))

    for fd, event in events:
        # fd为当前服务器socket，表示有新连接
        if fd == serversocket.fileno():
            connection, address = serversocket.accept()
            print("新连接：", address)
            # 新连接socket设置为非阻塞
            connection.setblocking(False)
            # 注册新连接fd到待读事件集合
            epoll.register(connection.fileno(), select.EPOLLIN)
            # 把新连接的文件句柄以及对象保存到字典
            connections[connection.fileno()] = connection
            # 以新连接的对象为键值，值存储在队列中，保存每个连接的信息
            message_queues[connection] = queue.Queue()
    
        # 关闭事件
        elif event & select.EPOLLHUP:
            print('客户端关闭')
            # 在epoll中注销客户端的文件句柄
            epoll.unregister(fd)
            # 关闭客户端的文件句柄
            connections[fd].close()
            # 在字典中删除与已关闭客户端相关的信息
            del connections[fd]

        # 可读事件
        elif event & select.EPOLLIN:
            # 接收数据
            data = connections[fd].recv(1024)
            if data:
                print("客户端%s收到数据：%s" % (connections[fd].getpeername(), data))
                # 将数据放入对应客户端的字典
                message_queues[connections[fd]].put(data)
                # 修改读取到消息的连接到等待写事件集合(即对应客户端收到消息后，再将其fd修改并加入写事件集合)
                epoll.modify(fd, select.EPOLLOUT)
            else:
                print('closing', address, 'after reading no data')
                epoll.unregister(fd)
                connections[fd].close()
                del connections[fd]

        # 可写事件
        elif event & select.EPOLLOUT:
            try:
                # 从字典中获取对应客户端的信息
                send_data = message_queues[connections[fd]].get_nowait()
            except queue.Empty:
                print(connections[fd].getpeername(), " queue empty")
                # 修改文件句柄为读事件
                epoll.modify(fd, select.EPOLLIN)
            else:
                print("客户端%s发送数据：%s" % (connections[fd].getpeername(), data))
                # 发送数据
                connections[fd].send(send_data)

# 在epoll中注销服务端文件句柄
epoll.unregister(serversocket.fileno())
# 关闭epoll
epoll.close()
# 关闭服务器socket
serversocket.close()
