#!usr/bin/python
# -*- coding:utf8 -*-
from flask import g
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 如果有用户id, 正常访问视图
        if g.userid:
            return f(*args, **kwargs)
        # 如果没有(未登录),返回错误信息
        else:
            return {'message': 'Invalid Token', 'data': None}, 401

    return wrapper
