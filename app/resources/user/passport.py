#!usr/bin/python
# -*- coding:utf8 -*-
"""用于存放用户认证相关的视图函数"""
import random
from app import db
from app import redis_client
from models.user import User
from datetime import datetime
from flask import current_app
from datetime import timedelta
from flask_restful import Resource
from sqlalchemy.orm import load_only
from flask_restful.inputs import regex
from utils.jwt_util import generate_jwt
from utils.constants import SMS_CODE_EXPIRE
from utils.parser import mobile as mobile_type
from flask_restful.reqparse import RequestParser


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


class LoginResource(Resource):
    """注册登录"""
    def post(self):
        # 获取参数
        parser = RequestParser()
        parser.add_argument('mobile', required=True, location='json', type=mobile_type)
        parser.add_argument('code', required=True, location='json', type=regex(r'^\d{6}$'))
        args = parser.parse_args()
        mobile = args.mobile
        code = args.code
        # 校验短信验证码
        key = 'app:code:{}'.format(mobile)
        real_code = redis_client.get(key)
        if not real_code or real_code != code:
            return {'message': 'Invalid Code', 'data': None}, 400
        # 删除验证码
        redis_client.delete(key)
        # 查询数据库
        user = User.query.options(load_only(User.id)).filter(User.mobile == mobile).first()
        if user:
            user.last_login = datetime.now()
        else:
            user = User(mobile=mobile, name=mobile, last_login=datetime.now())
            db.session.add(user)
        db.session.commit()
        # 返回结果

        # 生成令牌
        token = generate_jwt({'userid': user.id},
                             datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRE_DAYS']))

        return {"token": token}, 201


























