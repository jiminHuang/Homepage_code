# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月03日 星期四 14时28分34秒
#
'''
    读取系统变量，当前位置等环境因素
'''
import os

def get_cookie_secret():
    return os.getenv('COOKIE_SECRET')

def get_mail_settings():
    return [
        os.getenv('MAIL_USER'),
        os.getenv('MAIL_PASSWD'),
    ]

def get_local_position(position):
    return os.path.join(os.path.dirname(__file__), position)
