#!usr/bin/python
# -*- coding:utf8 -*-
from flask import Blueprint
from flask_restful import Api
from . profile import CurrentUserResource
from utils.constants import BASE_URL_PRIFIX
from .passport import SMSCodeResource, LoginResource


# 创建蓝图对象
user_bp = Blueprint('user', __name__, url_prefix=BASE_URL_PRIFIX)

# 根据蓝图对象创建组件对象
user_api = Api(user_bp)

# 设置json包装格式
from utils.output import output_json
user_api.representation('application/json')(output_json)

# 组件添加类视图
# user_api.add_resource(SMSCodeResource, '/sms/codes/<mobile>')  # 不加路由转换器路径
user_api.add_resource(SMSCodeResource, '/sms/codes/<mob:mobile>')
user_api.add_resource(LoginResource, '/authorizations')
user_api.add_resource(CurrentUserResource, '/user')

































