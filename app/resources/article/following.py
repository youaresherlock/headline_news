#!usr/bin/python
# -*- coding:utf8 -*-
from app import db
from flask import g
from datetime import datetime
from flask_restful import Resource 
from sqlalchemy.orm import load_only
from models.user import User, Relation
from utils.decorators import login_required
from flask_restful.reqparse import RequestParser


class FollowUserResource(Resource):
    method_decorators = {'post': [login_required]}

    def post(self):
        # 获取参数
        userid = g.userid
        parser = RequestParser()
        parser.add_argument('target', required=True, location='json', type=int)
        args = parser.parse_args()
        author_id = args.target

        # 查询该用户和作者是否有关系
        rel_obj = Relation.query.options(load_only(Relation.id)).\
            filter(Relation.user_id == userid, Relation.author_id == author_id).first()

        # 如果有关系, 更新记录
        if rel_obj:
            rel_obj.relation = Relation.RELATION.FOLLOW
            rel_obj.update_time = datetime.now()
        else:  # 如果无关系,添加记录
            rel_obj = Relation(user_id=userid, author_id=author_id, relation=Relation.RELATION.FOLLOW)
            db.session.add(rel_obj)

        # 让作者的粉丝数量+1
        User.query.filter(User.id == author_id).update({'fans_count': User.fans_count + 1})
        # 让用户的关注数量+1
        User.query.filter(User.id == userid).update({'following_count': User.following_count + 1})

        db.session.commit()

        # 返回结果
        return {'target': author_id}



























