# -*- coding: utf-8 -*-
'''
@Date: 2020-03-04 07:21:05
@LastEditors: fzzjj2008
@LastEditTime: 2020-03-04 07:23:06
'''
import asyncio

async def hello():
    print("Hello world!")
    # 异步调用asyncio.sleep(1):
    await asyncio.sleep(1)
    print("Hello again!")

# 获取EventLoop:
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(hello())
loop.close()