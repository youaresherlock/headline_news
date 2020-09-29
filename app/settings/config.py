#!usr/bin/python
# -*- coding:utf8 -*-


class DefaultConfig(object):
    """默认配置"""
    # mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:x1430371727@127.0.0.1:3306/top_news'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据变化
    SQLALCHEMY_ECHO = True  # 是否打印底层执行的SQL

    # redis配置
    REDIS_HOST = '127.0.0.1'  # ip
    REDIS_PORT = 6379  # 端口


# 定义字典记录 配置类型和配置子类的关系
config_dict = {
    'dev': DefaultConfig
}















