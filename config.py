# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月22日 星期二 21时45分15秒
#
'''
    读取配置文件
'''
from ConfigParser import SafeConfigParser

#读取配置文件
_config = SafeConfigParser()
_config.read('config.ini')

def get_database_address():
    return _config.get('database', 'address')

def get_database_port():
    return _config.get('database', 'port')

def get_database_user():
    return _config.get('database', 'user')

def get_database_password():
    return _config.get('database', 'password')


