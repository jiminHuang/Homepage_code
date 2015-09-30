# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月24日 星期四 20时38分27秒
#
'''
    时间处理time chewer的测试文件
'''
import timechewer
from nose.tools import *
import mock
import logging
from datetime import datetime

def test_strftime_present():
    #异常输入
    assert_raises(TypeError, timechewer.strftime_present)
    assert_raises(TypeError, timechewer.strftime_present, 1)
    assert_equal(timechewer.strftime_present(None, 1), 'Unknown')
    
    #正常输入
    assert_equal(
        timechewer.strftime_present("%m/%Y", datetime(2010, 04, 06)),
        '04/2010'
    );
    
    #persent
    assert_equal(
        timechewer.strftime_present("%m/%Y", None),
        'Present'
    );
