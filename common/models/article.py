#!usr/bin/python
# -*- coding:utf8 -*-
from app import db


class Channel(db.Model):
    """新闻频道"""
    __tablename__ = 'news_channel'

    id = db.Column(db.Integer, primary_key=True, doc='频道id')
    name = db.Column(db.String(30), doc='频道名称')
    is_default = db.Column(db.Boolean, default=False, doc='是否默认频道')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class UserChannel(db.Model):
    """用户关注频道表"""
    __tablename__ = 'news_user_channel'

    id = db.Column(db.Integer, primary_key=True, doc='主键id')
    user_id = db.Column(db.Integer, doc='用户id')
    channel_id = db.Column(db.Integer, doc='频道id')
    sequence = db.Column(db.Integer, default=0, doc='序号')
    is_deleted = db.Column(db.Boolean, default=False, doc='是否删除')

























