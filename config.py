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
import sys
import os

#配置文件设定
CONFIG_SETTINGS = {
    'MYSQL_ADDRESS' : 'database',
    'MYSQL_PORT' : 'database',
    'MYSQL_USER' : 'database',
    'MYSQL_PASSWD' : 'database',
    'MAIL_USER' : 'mail',
    'MAIL_PASSWD' : 'mail',
    'COOKIE_SECRET' : 'cookie',        
}

class _Config(object):
    '''
        配置类
    '''
    #读取配置文件
    _config = SafeConfigParser()
    _config.read('config.ini')

    
    def __getattr__(self, attr):
        '''
            重新定义获取属性方法
            使得先在环境中后在config文件中搜索
        '''

        if os.environ.get(attr, None) is not None:
            return os.environ.get(attr)
        
        try:
            return self._config.get(CONFIG_SETTINGS.get(attr, None), attr)
        except Exception:
            return None

    def get_local_position(self, position):
        '''
            获取当前位置
        '''
        return os.path.join(os.path.dirname(__file__), position)

Config = _Config()
