# encoding=utf8


__author__ = "张子豪"

"""
协程 web 应用
"""

import logging; logging.basicConfig(level=logging.INFO)  # 设置日志输出等级

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web


def index(request):  # 来自用户的请求信息会存在request对象中
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)  # 创建一个服务器对象，同时要指定一个事件循环
    app.router.add_route('GET', '/', index)  # 绑定url和函数
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)  # 绑定ip和port
    logging.info('server started at http://127.0.0.1:9000...')


loop = asyncio.get_event_loop()  # 获得一个循环事件
loop.run_until_complete(init(loop))  # 将coroutine放入循环事件当中

loop.run_forever()