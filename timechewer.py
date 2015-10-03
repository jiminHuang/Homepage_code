# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月24日 星期四 20时35分30秒
#
'''
    时间处理
'''

import datetime

def strftime_present(time_format, c_time):
    '''
        加入了对present检测的strftime
    '''
    if c_time is None:
        return 'Present'

    if time_format is None\
        or (not isinstance(c_time, datetime.datetime)\
            and not isinstance(c_time, datetime.date)):
        return 'Unknown'
    
    return c_time.strftime(time_format)
