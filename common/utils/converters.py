#!usr/bin/python
# -*- coding:utf8 -*-
from werkzeug.routing import BaseConverter


class MobileConverter(BaseConverter):
    """手机号格式"""
    regex = r'1[3-9]\d{9}'


def register_converters(app):
    """
    向flask app中添加转换器
    :param app:
    :return:
    """
    app.url_map.converters['mob'] = MobileConverter
































