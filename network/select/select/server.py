# -*- coding: utf-8 -*-
'''
@Date: 2020-03-05 00:13:35
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-06 00:05:07
'''
from socket import socket, AF_INET, SOCK_STREAM
from select import select
from queue import Queue, Empty

# TCP server
server = socket(AF_INET, SOCK_STREAM)
server.setblocking(False)
server.bind(('localhost', 8090))
# 最大监听连接数为5
server.listen(5)
# 定义集合
inputs = [server]
outputs = []
# 定义消息队列，实现读写分离
message_queues = {}

print('开始select监听')
while True:
    # inputs代表readset可读集合，outputs代表writeset可写集合，后面的inputs是exceptset异常集合
    # 阻塞时间为1s，不写表示当监听的描述符发生变化继续执行
    rlist, wlist, elist = select(inputs, outputs, inputs, 1)
    # print('监听中...')

    # 遍历读列表
    for s in rlist:
        if s is server:
            # 有新用户连接
            conn, addr = s.accept()            
            print('新用户连接：', addr)
            conn.setblocking(False)
            # 连接对象放到inputs里面
            inputs.append(conn)
            # 消息队列字典中，保存客户端数据
            message_queues[conn] = Queue()
        else:
            # 有老用户发消息, 处理接受
            data = s.recv(1024)
            if data:
                print('收到%s消息：%s' % (s.getpeername(), data.decode('utf-8')))
                # 将收到的消息存入对应的消息队列中
                message_queues[s].put(data)
                # 这里触发select的wlist返回数据
                if s not in outputs:
                    outputs.append(s)
            else:
                print('客户端断开连接', s.getpeername())
                # 移除连接
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                # 移除对应的消息队列
                del message_queues[s]

    # 遍历写列表
    for s in wlist:
        try:
            # 如果消息队列中有消息，从消息队列中获取要发送的消息
            send_data = message_queues[s].get_nowait()
        except Empty:
            print('客户端断开连接', s.getpeername())
            outputs.remove(s)
        else:
            print('发送%s消息：%s' % (s.getpeername(), send_data))
            s.send(send_data)
            outputs.remove(s)
        # del message_queues[s]

    # 遍历错误列表
    for s in elist:
        print ('异常发生：', s.getpeername())
        # 停止连接
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        # 消息消息队列
        del message_queues[s]

server.close()
