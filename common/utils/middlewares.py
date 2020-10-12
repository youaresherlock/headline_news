#!usr/bin/python
# -*- coding:utf8 -*-
from flask import request, g
from utils.jwt_util import verify_jwt


# @app.before_request
def get_user_info():
    """获取用户id"""
    # 从请求头中获取token
    token = request.headers.get('Authorization')

    g.userid = None
    # 验证token
    if token:
        data = verify_jwt(token)

        if data:
            # 取出用户id,使用g变量记录
            g.userid = data.get('userid')
