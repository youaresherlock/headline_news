#!usr/bin/python
# -*- coding:utf8 -*-
import jwt
from flask import current_app


def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload: dict荷载
    :param expiry: datetime有效期
    :param secret: 密钥
    :return: jwt
    """
    _payload = {'exp': expiry}
    _payload.update(payload)

    if not secret:
        secret = current_app.config['JWT_SECRET']
        token = jwt.encode(_payload, secret, algorithm='HS256')

        return token.decode()


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: payload
    """
    if not secret:
        secret = current_app.config['JWT_SECRET']
    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
    except jwt.PyJWTError:
        payload = None

    return payload


































