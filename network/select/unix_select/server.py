# -*- coding: utf-8 -*-
# Create on: 2020/06/01 13:53:49
# Author   : zhaojiajie

import os
import threading
from socket import socket, AF_UNIX, SOCK_STREAM
from select import select
from queue import Queue, Empty


class SingletonBase(type):
    """
    单例元类
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonBase, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class UnixServer(metaclass=SingletonBase):

    SOCK_ADDR = "/tmp/unix_sock"

    def __init__(self):
        self.server = None
        self.thread = None
        # 定义集合
        self.inputs = []
        self.outputs = []
        # 定义消息队列，实现读写分离
        self.message_queues = {}

    def create_sock(self):
        # TCP server
        print('创建socket')
        self.server = socket(AF_UNIX, SOCK_STREAM)
        if os.path.exists(self.SOCK_ADDR):
            os.unlink(self.SOCK_ADDR)
        self.server.setblocking(False)
        self.server.bind(self.SOCK_ADDR)
        # 最大监听连接数为5
        self.server.listen(5)
        # 初始化集合
        self.inputs = [self.server]
        self.outputs = []

    def listen_sock(self):
        print('开始select监听')
        while True:
            # inputs代表readset可读集合，outputs代表writeset可写集合，后面的inputs是exceptset异常集合
            # 阻塞时间为1s，不写表示当监听的描述符发生变化继续执行
            rlist, wlist, elist = select(self.inputs, self.outputs, self.inputs, 1)
            # print('监听中...')

            # 遍历读列表
            for s in rlist:
                if s is self.server:
                    # 有新用户连接
                    conn, addr = s.accept()
                    print('新用户连接：', addr)
                    conn.setblocking(False)
                    # 连接对象放到inputs里面
                    self.inputs.append(conn)
                    # 消息队列字典中，保存客户端数据
                    self.message_queues[conn] = Queue()
                else:
                    # 有老用户发消息, 处理接受
                    data = s.recv(1024)
                    if data:    
                        print('收到%s消息：%s' % (s.getpeername(), data.decode('utf-8')))
                    else:
                        print('客户端断开连接', s.getpeername())
                        # 移除连接
                        if s in self.outputs:
                            self.outputs.remove(s)
                        self.inputs.remove(s)
                        s.close()
                        # 移除对应的消息队列
                        del self.message_queues[s]

            # 遍历写列表
            for s in wlist:
                try:
                    # 如果消息队列中有消息，从消息队列中获取要发送的消息
                    send_data = self.message_queues[s].get_nowait()
                except Empty:
                    print('客户端断开连接', s.getpeername())
                    self.outputs.remove(s)
                else:
                    print('发送%s消息：%s' % (s.getpeername(), send_data))
                    s.send(send_data)
                    self.outputs.remove(s)
                # del message_queues[s]

            # 遍历错误列表
            for s in elist:
                print ('异常发生：', s.getpeername())
                # 停止连接
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                # 消息消息队列
                del self.message_queues[s]

        self.server.close()

    def send_all(self, data):
        for s in self.message_queues:
            # 这里触发select的wlist返回数据
            self.message_queues[s].put(data)
            if s not in self.outputs:
                self.outputs.append(s)

    def start(self):
        self.create_sock()
        self.thread = threading.Thread(target=self.listen_sock)
        self.thread.daemon = False
        self.thread.start()


if __name__ == "__main__":
    # 创建socket
    UnixServer().start()
    # 发送消息到所有客户端
    while True:
        data = input('>>').strip()
        if data:
            UnixServer().send_all(data.encode('utf-8'))
