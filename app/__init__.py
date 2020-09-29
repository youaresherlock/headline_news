#!usr/bin/python
# -*- coding:utf8 -*-
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import dirname, abspath

# 将common路径添加到模块查询路径中
BASE_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, BASE_DIR + '/common')

from app.settings.config import config_dict
from utils.constants import EXTRA_ENV_COINFIG


# sqlalchemy组件对象
db = SQLAlchemy()


def register_extensions(app):
    """组件初始化"""

    # 延后关联sqlalchemy
    db.init_app(app)


def create_flask_app(type):
    """
    创建flask应用
    :param type: 配置类型
    :return: flask应用
    """
    # 创建flask应用
    flask_app = Flask(__name__)
    # 根据配置类型取出配置子类
    config_class = config_dict[type]
    # 先从默认配置中加载
    flask_app.config.from_object(config_class)
    # 再从额外配置中加载
    flask_app.config.from_envvar(EXTRA_ENV_COINFIG, silent=True)

    # 返回应用
    return flask_app


def create_app(type):
    """创建flask应用 和 初始化组件"""

    app = create_flask_app(type)

    # 组件初始化
    register_extensions(app)

    return app































