#!usr/bin/python
# -*- coding:utf8 -*-
from app import db
from models.user import User
from datetime import datetime
from models.article import Article
from flask_restful import Resource
from models.article import ArticleContent
from utils.constants import HOME_PRE_PAGE
from flask_restful.reqparse import RequestParser


class ArticleListResource(Resource):
    @property
    def get(self):
        # 获取参数 前端传递频道id以及毫秒的时间戳
        parser = RequestParser()
        parser.add_argument('channel_id', required=True, location='args', type=int)
        parser.add_argument('timestamp', required=True, location='args', type=int)
        args = parser.parse_args()
        channel_id = args.channel_id
        timestamp = args.timestamp
        # 如果为"推荐频道", 则返回空数据
        if channel_id == 0:
            return {'results': [], 'pre_timestamp': 0}

        # 将时间戳转换为日期时间对象
        date = datetime.fromtimestamp(timestamp * 0.001)
        # 数据库查询 指定频道 & 审核通过 & 发布时间 < 时间戳 & 时间倒序 & 分页
        data = db.session.query(Article.id, Article.title, Article.user_id, Article.ctime, User.name,
                                Article.comment_count, Article.cover).\
            join(User, Article.user_id == User.id).\
            filter(Article.channel_id == channel_id, Article.status == Article.STATUS.APPROVED,
                   Article.ctime < date).\
            order_by(Article.ctime.desc()).limit(HOME_PRE_PAGE).all()
        # 序列化
        articles = [
            {
                'art_id': item.id,
                'title': item.title,
                'aut_id': item.user_id,
                'pubdate': item.ctime.isoformat(),
                'aut_name': item.name,
                'comm_count': item.comment_count,
                'cover': item.cover
            }
            for item in data
        ]
        # 构建响应数据
        # 将日期时间对象转为时间戳
        pre_timestamp = int(data[-1].ctime.timestamp() * 1000) if date else 0
        # 返回响应
        return {'results': articles, 'pre_timestamp': pre_timestamp}


class ArticleDetailResource(Resource):
    def get(self, article_id):
        """
        查询来自两部分
        基础数据 文章/作者数据
        关系数据 关注/点赞/收藏数据
        :param article_id:
        :return:
        """
        # 根据文章id查询文章数据
        data = db.session.\
            query(Article.id, Article.title, Article.ctime, Article.user_id, User.name, User.profile_photo, ArticleContent.content).\
            join(User, Article.user_id == User.id).\
            join(ArticleContent, ArticleContent.article_id == Article.id).\
            filter(Article.id == article_id).first()

        # 序列化处理
        article_dict = {
            'art_id': data.id,
            'title': data.title,
            'pubdate': data.ctime.isoformat(),
            'aut_id': data.user_id,
            'aut_name': data.name,
            'aut_photo': data.profile_photo,
            'content': data.content,
            'is_followed': False,
            'attitude': -1,
            'is_collected': False
        }

        # 返回数据
        return article_dict





























