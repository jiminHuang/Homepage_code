# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月22日 星期二 21时46分02秒
#
'''
    配置变量的测试文件
'''

from nose.tools import *
import config

def test_get_database_address():
    '''
        测试获取数据库地址
    '''
    address = config.get_database_address()
    assert address is not None

def test_get_database_port():
    '''
        测试获取数据库接口
    '''
    port = config.get_database_port()
    assert port is not None


def test_get_database_user():
    '''
        测试获取数据库地址
    '''
    user = config.get_database_user()
    assert user is not None

def test_get_database_password():
    '''
        测试获取数据库密码
    '''
    password = config.get_database_password()
    assert password is not None
