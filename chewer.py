# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年10月03日 星期六 15时45分11秒
#
'''
    后续处理方法文件
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

def this_year():
    '''
        获取当前时间的年份
    ''' 
    return strftime_present("%Y", datetime.datetime.now())

def static_image(image, suffix='jpeg'):
    '''
        处理image 转化为伪静态地址
    '''
    if image is None:
        return None
    
    return ''.join(('img/', str(image), '.', suffix))

def text_cutter(text, length, suffix='...'):
    '''
        处理字符串，截取指定位数并添加末尾
    ''' 
    if text is None or not isinstance(text, basestring):
        return ''
    
    return ''.join(
        (
            text[:length],
            suffix if len(text) > length else '',
        )
    )
