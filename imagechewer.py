# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月29日 星期二 10时13分04秒
#
'''
    image 地址处理
'''
def static_image(image, suffix='jpeg'):
    '''
        处理image 转化为伪静态地址
    '''
    if image is None:
        return None
    
    return ''.join(('img/', str(image), '.', suffix))
