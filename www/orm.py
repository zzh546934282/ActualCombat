#　encoding=utf8


__author__ = '张子豪'

import asyncio, logging

import aiomysql


def log(sql, args=()):
    logging.info('SQL: %s' % sql)


@asyncio.coroutine
def crete_poool(loop, **kw):  # 创建一个数据库连接池
    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(  # 创建一个连接池,只要涉及到创建连接都会比较耽误时间，
        host=kw.get('host', 'localhost'),  # 数据库的链接地址
        port=kw.get('port', 3306),  # 端口号
        user=kw['user'],  # 数据库的用户名
        password=kw['password'],  # 数据库的密码
        db=kw['db'],   # 连接的数据库名
        charset=kw.get('charset', 'utf8'),  # 指定编码格式
        autocommit=kw.get('autocommit', True),   # 自动提交事务
        maxsize=kw.get('maxsize', 10),  # 最大连接数为10
        minsize=kw.get('minsize', 1),  # 最小连接数为1
        loop=loop
   )


@asyncio.coroutine
def select(sql, args, size=None):
    log(sql, args)
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs



