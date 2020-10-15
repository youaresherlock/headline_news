#!usr/bin/python
# -*- coding:utf8 -*-
from flask_restful import Resource
from models.article import Channel
from sqlalchemy.orm import load_only


class AllChannelResource(Resource):
    """所有频道"""
    def get(self):
        # 查询所有的频道
        channels = Channel.query.options(load_only(Channel.id, Channel.name)).all()

        # 序列化
        channel_list = [channel.to_dict() for channel in channels]

        return {'channels': channel_list}






















