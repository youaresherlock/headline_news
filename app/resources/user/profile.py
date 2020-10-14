#!usr/bin/python
# -*- coding:utf8 -*-
from app import db
from flask import g
from models.user import User
from flask_restful import Resource
from utils.parser import image_file
from sqlalchemy.orm import load_only
from utils.img_storage import upload_file
from utils.decorators import login_required
from flask_restful.reqparse import RequestParser


class CurrentUserResource(Resource):
    method_decorators = {'get': [login_required]}

    def get(self):
        """获取用户信息"""
        userid = g.userid

        user = User.query.options(load_only(User.id,
                                            User.name,
                                            User.profile_photo,
                                            User.introduction,
                                            User.article_count,
                                            User.following_count,
                                            User.fans_count)).filter(User.id == userid).first()

        # 序列化返回数据
        return user.to_dict()


class UserPhotoResource(Resource):
    method_decorators = [login_required]

    # 进行局部更新,使用patch
    def patch(self):
        """修改头像"""

        # 获取参数
        userid = g.userid
        parser = RequestParser()
        parser.add_argument('photo', required=True, location='files', type=image_file)
        args = parser.parse_args()
        photo_file = args.photo
        # 获取二进制数据
        file_bytes = photo_file.read()
        # 上传到七牛云,返回图片URl
        try:
            file_url = upload_file(file_bytes)
        except Exception as e:
            return {'message': 'Third Error: %s' % e}, 500
        # 到数据库中更新头像URL
        User.query.filter(User.id == userid).update({'profile_photo': file_url})
        db.session.commit()
        # 返回URL
        return {'photo_url': file_url}
















