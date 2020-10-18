#!usr/bin/python
# -*- coding:utf8 -*-
from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import DATETIME


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


class Article(db.Model):
    """文章基本信息表"""
    __tablename__ = 'news_article_basic'

    class STATUS:
        DRAFT = 0  # 草稿
        UNREVIEWED = 1  # 待审核
        APPROVED = 2  # 审核通过
        FAILED = 3  # 审核失败
        DELETED = 4  # 已删除
        BANNED = 5  # 封禁

    id = db.Column(db.Integer, primary_key=True, doc='文章id')
    user_id = db.Column(db.Integer, doc='用户id')
    channel_id = db.Column(db.Integer, doc='频道id')
    title = db.Column(db.String(130), doc='标题')
    cover = db.Column(db.JSON, doc='封面')
    # db.Datetime对应MYSQL的字段时datetime数据类型,以YYYY-MM-DD HH:MM:SS显示
    # MYSQL提供了另一种类似于DATETIME, 叫做TIMESTAMP的时间数据类型
    # ctime = db.Column(db.Datetime, default=datetime.now, doc='创建时间')
    # 进行flask db migrate进行数据迁移发现不了字段的改变，使用SQL语句进行修改
    # alter table news_article_basic modify column ctime datetime(3);
    ctime = db.Column(DATETIME(fsp=3), default=datetime.now, doc='创建时间')
    status = db.Column(db.Integer, default=0, doc='帖文状态')
    comment_count = db.Column(db.Integer, default=0, doc='评论数')


class ArticleContent(db.Model):
    """文章内容表"""
    __tablename__ = 'news_article_content'

    article_id = db.Column(db.Integer, primary_key=True, doc='文章id')
    content = db.Column(db.Text, doc='贴文内容')























