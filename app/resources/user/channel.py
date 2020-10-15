#!usr/bin/python
# -*- coding:utf8 -*-
from flask import g
from flask_restful import Resource
from models.article import Channel
from sqlalchemy.orm import load_only
from models.article import UserChannel


class UserChannelResource(Resource):

    def get(self):
        # 获取参数
        userid = g.userid
        if userid:  # 判断用户是否登录
            # 如果登录,查询用户频道
            channels = Channel.query.options(load_only(Channel.id, Channel.name)).\
                join(UserChannel, Channel.id == UserChannel.channel_id).\
                filter(UserChannel.user_id == userid, UserChannel.is_deleted is False).\
                order_by(UserChannel.sequence).all()
            if len(channels) == 0:  # 用户未选择过频道,则查询默认频道
                channels = Channel.query.options(load_only(Channel.id, Channel.name)). \
                    filter(Channel.is_default is True).all()
        else:
            # 未登录,查询默认频道
            channels = Channel.query.options(load_only(Channel.id, Channel.name)).\
                filter(Channel.is_default is True).all()

        # 序列化
        channel_list = [channel.to_dict() for channel in channels]
        # 手动添加"推荐频道", 数据库中没有保存该频道的数据, 该频道数据由推荐系统返回
        channel_list.insert(0, {'id': 0, 'name': '推荐'})
        # 返回数据

        return {'channels': channel_list}

























