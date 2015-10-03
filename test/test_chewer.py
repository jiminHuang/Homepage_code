# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年10月03日 星期六 15时43分22秒
#
import chewer
from nose.tools import *
import mock
import logging
from datetime import datetime

'''
    后续处理方法测试文件
'''

def test_static_image():
    #image未输入
    assert_raises(TypeError, chewer.static_image)
    
    #image输入为空
    assert chewer.static_image(None) is None
    
    #默认输入image
    assert_equal(
        chewer.static_image('test'),
        'img/test.jpeg'
    )
    
    #测试输入image其他后缀
    assert_equal(
        chewer.static_image('test', 'png'),
        'img/test.png'
    )

def test_strftime_present():
    #异常输入
    assert_raises(TypeError, chewer.strftime_present)
    assert_raises(TypeError, chewer.strftime_present, 1)
    assert_equal(chewer.strftime_present(None, 1), 'Unknown')
    
    #正常输入
    assert_equal(
        chewer.strftime_present("%m/%Y", datetime(2010, 04, 06)),
        '04/2010'
    );
    
    #persent
    assert_equal(
        chewer.strftime_present("%m/%Y", None),
        'Present'
    );

def test_text_cutter():
    #异常输入
    assert_raises(TypeError, chewer.text_cutter)
    assert_raises(TypeError, chewer.text_cutter, 1)
    assert_equal(chewer.text_cutter(None, 1), '')
    assert_equal(chewer.text_cutter(3, 1), '')
    
    #正常输入
    assert_equal(
        chewer.text_cutter('test', 1),
        't...'
    )

    assert_equal(
        chewer.text_cutter('test', 6),
        'test'
    )
