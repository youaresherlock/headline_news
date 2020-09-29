#!usr/bin/python
# -*- coding:utf8 -*-
"""用于存放用户认证相关的视图函数"""
from flask_restful import Resource


class SMSCodeResource(Resource):
    """获取短信验证码"""
    def get(self):
        return {'foo': 'get'}