#!usr/bin/python
# -*- coding:utf8 -*-
"""用于存放用户认证相关的视图函数"""
import random
from app import redis_client
from flask_restful import Resource
from utils.constants import SMS_CODE_EXPIRE


class SMSCodeResource(Resource):
    """获取短信验证码"""
    def get(self, mobile):
        # 生成验证码
        rand_num = '%06d' % random.randint(0, 999999)
        # 保存验证码 app:code:xxxxx 123456
        key = 'app:code:{}'.format(mobile)
        redis_client.set(key, rand_num, ex=SMS_CODE_EXPIRE)
        # 发送短信
        print('短信验证码: "mobile": {}, "code": {}'.format(mobile, rand_num))
        # 返回结果

        return {'mobile': mobile}


























