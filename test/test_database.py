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
import logging

@mock.patch.object(logging, "error")
def test_typelist_getitem(mock_logging_error):
    '''
        测试Typelist list扩展类的取方法
    '''
    example = database.TypeList([1])
    
    #越界异常
    test_result = example[2]
    assert mock_logging_error.called 
    assert_equal(test_result, 'Unknown')
    
    #正常输入
    assert_equal(example[1], 1)


class TestPersistence(object):
    '''
        持久化对象测试类
    '''

    def setUp(self):
        '''
            持久化对象测试初始化
        '''
        #捕获数据库连接并用mock模拟
        self.mock_db = mock.Mock()
        patch = mock.patch('database._get_connection')
        self.mock_connection = patch.start()
        self.mock_connection.return_value = self.mock_db

    def test_user_get(self):
        '''
            测试user get函数
        '''
        #user_id未输入
        user = database.User.get()
        assert user is None
        
        #mock构建
        mock_user = mock.Mock()
        mock_user.type = 1
        self.mock_db.get.return_value = mock_user
        
        #user_id输入
        user = database.User.get(user_id=1)
        self.mock_db.get.assert_called_with('SELECT * FROM user WHERE user_id = %s', 1)
        
        #username输入
        mock_user.type = 1
        user = database.User.get(username=1)
        self.mock_db.get.assert_called_with('SELECT * FROM user WHERE username = %s', 1)
        
        #user不存在
        self.mock_db.get.return_value = None
        user = database.User.get(username=1)
        assert user is None

    def test_background_query(self):
        '''
            测试background query函数 异常输入
        '''
        #user_id未输入
        assert_raises(TypeError, database.Background.query)

        #user_id输入为空
        user = database.Background.query(None)
        assert user is None
        
        #mock构建
        mock_background = mock.Mock()
        mock_background.background_type = 1
        self.mock_db.query.return_value = [mock_background]
    
        #user_id正常输入
        backgrounds = database.Background.query(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_background '
                'NATURAL JOIN background '
                'WHERE user_id = %s'
            ),
            1
        )
        assert_equal(backgrounds, [mock_background])
        
        #backgrounds无
        self.mock_db.query.return_value = []
        backgrounds = database.Background.query(1)
        assert_equal(backgrounds, [])
        
    def test_experience_query(self):
        '''
            测试experience query函数 异常输入
        '''
        #user_id未输入
        assert_raises(TypeError, database.Experience.query)

        #user_id输入为空
        user = database.Experience.query(None)
        assert user is None
        
        #mock构建
        mock_experience = mock.Mock()
        self.mock_db.query.return_value = [mock_experience]
        
        #user_id正常输入
        experiences = database.Experience.query(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_experience '
                'NATURAL JOIN experience '
                'WHERE user_id = %s'
            ),
            1
        )
        assert_equal(experiences, [mock_experience])
    
    def test_interests_query(self):
        '''
            测试interests query函数
        '''
        #user_id未输入
        assert_raises(TypeError, database.Interests.query)

        #user_id输入为空
        user = database.Interests.query(None)
        assert user is None
        
        #mock构建
        mock_interests = mock.Mock()
        self.mock_db.query.return_value = [mock_interests]
        
        #user_id正常输入
        interests = database.Interests.query(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_interests '
                'NATURAL JOIN interests '
                'WHERE user_id = %s'
            ),
            1
        )
        assert_equal(interests, [mock_interests])
        
    def test_article_get(self):
        '''
            测试article get函数
        '''
        #article_id未输入
        assert_raises(TypeError, database.Article.get)
        
        #article_id输入为空
        article = database.Article.get(None) 
        assert article is None
        
        #mock构建
        mock_article = mock.Mock()
        mock_article.author = "1"
        self.mock_db.get.return_value = mock_article
        
        #正常输入
        with mock.patch.object(database.User, 'get'):
            article = database.Article.get(1)
            self.mock_db.get.assert_called_with(
                (
                    'SELECT * '
                    'FROM article '
                    'WHERE article_id = %s'
                ),
                1
            )
            database.User.get.assert_called_with(user_id="1")
            assert_equal(article, mock_article)
            #article未找到
            self.mock_db.get.return_value = None
            article = database.Article.get(1)
            assert article is None
