# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年10月03日 星期六 20时13分05秒
#
import config
import os
from nose.tools import *
import mock
import ConfigParser

@mock.patch('os.environ.get')
def test_getattr(mock_os):
    #环境变量可获取
    mock_os.return_value = 'test'
    assert_equal(config.Config.TEST_CONFIG, 'test')
    mock_os.assert_called_with('TEST_CONFIG')
    
    #环境变量不可获取
    mock_os.return_value = None
    #config中不存在
    assert_equal(config.Config.TEST_CONFIG, None)
    mock_os.assert_called_with('TEST_CONFIG', None)
    #config中存在
    with mock.patch('ConfigParser.SafeConfigParser.get'):
        ConfigParser.SafeConfigParser.get.return_value = 'test'
        assert_equal(config.Config.TEST_CONFIG, 'test')
