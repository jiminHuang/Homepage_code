# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月03日 星期四 15时03分28秒
#
'''
    环境变量的测试文件
'''

import os
import environment
from nose.tools import *

def test_get_cookie_secret():
    '''
        测试获取系统变量cookie secret
    '''
    os.environ['COOKIE_SECRET'] = 'test'
    assert_equal(environment.get_cookie_secret(), 'test')

def test_get_mail_settings():
    '''
        测试获取系统关于邮件的环境变量
    '''
    os.environ['MAIL_USER'] = 'test'
    os.environ['MAIL_PASSWD'] = 'test'
    assert_equal(environment.get_mail_settings(), ['test','test'])
