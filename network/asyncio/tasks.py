# -*- coding: utf-8 -*-
'''
@Date: 2020-03-04 07:22:45
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-04 07:22:58
'''
import threading
import asyncio

async def hello():
    print('Hello world! (%s)' % threading.currentThread())
    await asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()