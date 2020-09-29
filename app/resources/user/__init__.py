#!usr/bin/python
# -*- coding:utf8 -*-
from flask import Blueprint
from flask_restful import Api
from .passport import SMSCodeResource


# 创建蓝图对象
user_bp = Blueprint('user', __name__)

# 根据蓝图对象创建组件对象
user_api = Api(user_bp)

# 组件添加类视图
user_api.add_resource(SMSCodeResource, '/sms/codes')

































