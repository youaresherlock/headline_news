#!usr/bin/python
# -*- coding:utf8 -*-
from app import db
from flask import g
from flask_restful import Resource
from models.article import Article
from models.article import Comment
from flask_restful.inputs import regex
from utils.decorators import login_required
from flask_restful.reqparse import RequestParser


class CommentsResource(Resource):
    method_decorators = {'post': [login_required]}

    def post(self):
        """发布评论"""
        # 获取参数
        userid = g.userid
        parser = RequestParser()
        parser.add_argument('target', required=True, location='json', type=int)
        parser.add_argument('content', required=True, location='json', type=regex(r'.+'))
        args = parser.parse_args()
        target = args.target  # 文章id
        content = args.content  # 评论内容
        # 新增评论数据
        comment = Comment(user_id=userid, article_id=target, content=content, parent_id=0)
        db.session.add(comment)
        # 让文章的评论数量+1
        Article.query.filter(Article.id == target).update({'comment_count': Article.comment_count + 1})
        db.session.commit()
        # 返回结果

        return {'com_id': comment.id, 'target': target}