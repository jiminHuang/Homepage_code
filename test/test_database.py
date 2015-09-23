# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月23日 星期三 13时50分22秒
#
'''
    数据层测试文件
'''

from nose.tools import *
import database
import torndb
import mock

@mock.patch("torndb.Connection")
def test_user_get(mock_connection):
    '''
        测试user get函数
    '''
    #user_id未输入
    user = database.User.get()
    assert user is None
    
    #正常输入
    mock_get = mock.Mock()
    mock_get.get.return_value = 'test'
    mock_db = mock.Mock(return_value=mock_get)
    mock_connection = mock.Mock(return_value=mock_db)
    user = database.User.get(user_id=1)
    assert user is not None

@mock.patch("torndb.Connection")
def test_background_query(mock_connection):
    '''
        测试background query函数 异常输入
    '''
    #user_id未输入
    assert_raises(TypeError, database.User.get())

    #user_id输入为空
    user = database.User.get(None)
    assert user is None
