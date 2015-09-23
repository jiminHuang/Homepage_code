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
    db = 'user'

    @classmethod
    def get(cls, user_id):
        '''
            获取一个user信息
        '''
        #user_id 为空
        if user_id is None:
            return None
        
        #构建数据库连接
        connection = _get_connection(cls.db)
        
        sql = (
            'SELECT * '
            'FROM user '
            'WHERE user_id = {user_id}'
        ).format(user_id=user_id)
        
        return connection.get(sql)
