# -*- coding: utf-8 -*-
'''
@Date: 2020-03-08 18:57:07
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-08 23:16:44
'''
import gevent
from gevent.lock import Semaphore

sem = Semaphore(1)


def f1():
    for i in range(5):
        # sem.acquire()
        print('run f1, this is ', i)
        # sem.release()
        gevent.sleep(1)


def f2():
    for i in range(5):
        # sem.acquire()
        print('run f2, that is ', i)
        # sem.release()
        gevent.sleep(1)


t1 = gevent.spawn(f1)
t2 = gevent.spawn(f2)
gevent.joinall([t1, t2])