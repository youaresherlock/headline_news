#!usr/bin/python
# -*- coding:utf8 -*-
# 在article包的初始化文件中进行蓝图的初始化处理
from flask import Blueprint
from flask_restful import Api
from .comment import CommentsResource
from .channel import AllChannelResource
from .following import FollowUserResource
from .articles import ArticleListResource
from .articles import ArticleDetailResource
from .following import UnFollowUserResource
from utils.constants import BASE_URL_PRIFIX


# 1.创建蓝图对象
article_bp = Blueprint('article', __name__, url_prefix=BASE_URL_PRIFIX)

# 2.创建Api对象
article_api = Api(article_bp)

# 设置json包装格式
from utils.output import output_json
article_api.representation('application/json')(output_json)

article_api.add_resource(AllChannelResource, '/channels')
article_api.add_resource(ArticleListResource, '/articles')
article_api.add_resource(ArticleDetailResource, '/articles/<int:article_id>')
article_api.add_resource(FollowUserResource, '/user/followings')
article_api.add_resource(UnFollowUserResource, '/user/followings/<int:target>')
article_api.add_resource(CommentsResource, '/comments')





























