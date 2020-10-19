#!usr/bin/python
# -*- coding:utf8 -*-
from app import db
from flask import g
from models.user import User
from flask_restful import Resource
from models.article import Article
from models.article import Comment
from sqlalchemy.orm import load_only
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

    def get(self):
        """获取评论列表"""
        # 获取参数
        parser = RequestParser()
        parser.add_argument('source', required=True, location='args', type=int)  # 文章id
        parser.add_argument('offset', default=0, location='args', type=int)  # 评论id
        parser.add_argument('limit', default=10, location='args', type=int)  # 条数
        args = parser.parse_args()
        source = args.source
        offset = args.offset
        page_count = args.limit

        # 查询该文章的评论 & 分页(评论id > offset)
        data = db.session.query(Comment.id, Comment.user_id, User.name,
                                User.profile_photo,Comment.ctime,
                                Comment.content, Comment.reply_count,
                                Comment.like_count).\
            join(User, Comment.user_id == User.id).\
            filter(Comment.article_id == source, Comment.id > offset).\
            limit(page_count).all()

        comment_list = [
            {
                'com_id': item.id,
                'aud_id': item.user_id,
                'aut_name': item.name,
                'aut_photo': item.profile_photo,
                'pubdate': item.ctime.isoformat(),
                'content': item.content,
                'reply_count': item.reply_count,
                'like_count': item.like_count
            }
            for item in data
        ]
        # 查询评论的总数
        count = Comment.query.filter(Comment.article_id == source).count()
        # 所有评论中最后一条的id
        end_comment = Comment.query.options(load_only(Comment.id)).filter(Comment.article_id == source).order_by(Comment.id.desc()).first()
        end_id = end_comment.id if end_comment else None
        # 本次请求中最后一条的id
        last_id = data[-1].id if data else None

        return {'results': comment_list, 'total_count': count, 'end_id': end_id, 'last_id': last_id}


