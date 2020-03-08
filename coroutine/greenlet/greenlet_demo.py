# -*- coding: utf-8 -*-
'''
@Date: 2020-03-08 18:57:07
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-08 19:03:15
'''
from greenlet import greenlet
def test1():
    print(12)
    gr2.switch()
    print(34)

def test2():
    print(56)
    gr1.switch()
    print(78)

gr1 = greenlet(test1)
gr2 = greenlet(test2)
print('===============')
gr1.switch()
print('===============')
gr2.switch()
