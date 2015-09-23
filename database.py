# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月22日 星期二 21时40分29秒
#
'''
    数据层文件
    包括持久化和操作
'''
import torndb
import config
import logging

def _get_connection(db):
    '''
        获取数据库连接函数
    '''
    return torndb.Connection(
        ":".join(
            [config.get_database_address(),
            config.get_database_port()]
        ),
        db,
        config.get_database_user(),
        config.get_database_password(),
    )
    

class User(object):
    '''
        user表持久化
    '''
    db = 'homepage'
    USER_TYPE = [u'Mentor', u'Doctor', u'Graduate', u'UnderGraduate']

    @classmethod
    def _user_type(cls, ptype):
        '''
            获得person type
        '''
        try:
            return cls.USER_TYPE[ptype-1]
        except IndexError:
            logging.error('Person Type Index Exception')
            return 'Person Type Exception'

    @classmethod
    def get(cls, user_id=None, username=None):
        '''
            获取一个user信息
        '''
        #user_id 为空
        if user_id is None and username is None:
            return None
        
        #构建数据库连接
        connection = _get_connection(cls.db)
        
        sql =  'SELECT * FROM user '
        if user_id is not None:
            sql += 'WHERE user_id = %s'
            user = user_id
        else:
            sql += 'WHERE username = %s'
            user = username

        user = connection.get(sql, user)
        user.type = cls._user_type(user.type)
        return user

class Background(object):
    '''
        用户学历背景 background表持久化对象
    '''
    db = 'homepage'
    BACKGROUND_TYPE = ['Bachelor', 'Master', 'Ph.D']
    
    @classmethod
    def _background_type(cls, btype):
        try:
            return cls.BACKGROUND_TYPE[btype-1]
        except IndexError:
            logging.error('background type index error')
            return 'Background Type Error' 
    
    @classmethod
    def query(cls, user_id):
        '''
            根据user_id 获取对应user背景
        '''
        #user_is 为 None
        if user_id is None:
            return None
        
        #构建数据库连接
        connection = _get_connection(cls.db)
        
        sql = (
            'SELECT * '
            'FROM user_background '
            'NATURAL JOIN background '
            'WHERE user_id = %s'
        )
        
        backgrounds = connection.query(sql, user_id)
        for background in backgrounds:
            background.background_type =\
                cls._background_type(background.background_type)
        return backgrounds 
