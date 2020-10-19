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
    method_decorators = {'post': [login_required], 'get': [login_required]}

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

    def get(self):
        """获取关注列表"""
        # 获取参数
        userid = g.userid
        parser = RequestParser()
        parser.add_argument('page', default=1, location='args', type=int)
        parser.add_argument('per_page', default=10, location='args', type=int)
        args = parser.parse_args()
        page = args.page
        per_page = args.per_page

        # 数据查询 join代替关联查询 & 当前用户的关注列表 & 关注事件倒序 & 分页
        pn = User.query.options(load_only(User.id, User.name, User.profile_photo, User.fans)).\
            join(Relation, User.id == Relation.author_id).\
            filter(Relation.user_id == userid, Relation.relation == Relation.RELATION.FOLLOW).\
            order_by(Relation.update_time.desc()).paginate(page, per_page)

        data = [{
            'id': item.id, 
            'name': item.name,
            'photo': item.profile_photo,
            'fans_count': item.fans_count,
            'mutual_follow': False
        } for item in pn.items]

        return {'results': data, 'total_count': pn.total, 'per_page': per_page, 'page': pn.page}


class UnFollowUserResource(Resource):
    method_decorators = {'delete': [login_required]}

    def delete(self, target):
        """取消关注, DELETE方法具有幂等性"""
        # 获取参数
        userid = g.userid
        # 更新用户关系 删除关系, 将relation字段进行更新
        Relation.query.filter(Relation.user_id == userid, Relation.author_id == target, Relation.relation == Relation.RELATION.FOLLOW).\
            update({'relation': Relation.RELATION.DELETE, 'update_time': datetime.now()})
        # 让作者的粉丝数量-1
        User.query.filter(User.id == userid).update({'fans_count': User.fans_count - 1})
        # 让用户的关注数量-1
        User.query.filter(User.id == target).update({'following_count': User.following_count - 1})

        db.session.commit()

        # 返回结果
        return {'target': target}


























