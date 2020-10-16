#!usr/bin/python
# -*- coding:utf8 -*-
from app import db
from flask import g
from flask import request
from flask_restful import Resource
from models.article import Channel
from sqlalchemy.orm import load_only
from models.article import UserChannel
from utils.decorators import login_required


class UserChannelResource(Resource):
    method_decorators = {'put': [login_required]}

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

    def put(self):
        """修改用户频道 重置式更新"""
        # 获取参数
        userid = g.userid
        channels = request.json.get('channels')
        # 将该用户原有的频道列表逻辑删除
        UserChannel.query.filter(UserChannel.user_id == userid, UserChannel.is_deleted is False).\
            update({'is_deleted': True})
        # 遍历新的频道列表
        for channel in channels:
            # 查询是否关注过该频道
            user_channel = UserChannel.query.options(load_only(UserChannel.id)).filter(
                UserChannel.user_id == userid, UserChannel.channel_id == channel['id']
            ).first()
            if user_channel:  # 如果有, 更新数据(序号和逻辑删除去掉)
                user_channel.sequence = channel['seq']
                user_channel.is_deleted = False
            else:
                # 如果没有, 新增数据
                user_channel = UserChannel(user_id=userid, channel_id=channel['id'], sequence=channel['seq'])
                db.session.add(user_channel)
        # 将数据返回
        db.session.commit()

        return {'channels': channels}

























