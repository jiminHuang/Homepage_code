# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月29日 星期二 10时13分16秒
#
'''
    imagechewer的测试文件
'''
import imagechewer
from nose.tools import *

def test_static_image():
    #image未输入
    assert_raises(TypeError, imagechewer.static_image)
    
    #image输入为空
    assert imagechewer.static_image(None) is None
    
    #默认输入image
    assert_equal(
        imagechewer.static_image('test'),
        'img/test.jpeg'
    )
    
    #测试输入image其他后缀
    assert_equal(
        imagechewer.static_image('test', 'png'),
        'img/test.png'
    )
