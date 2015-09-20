# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月03日 星期四 14时26分03秒
#
import environment
import modules

settings = {
    'debug' : True, #调试选项，开启后每一次源文件的更改将会自动重启服务器(而不需要手动操作)
    'xsrf_cookies' : True,
    'login_url' : '/login', 
    'cookie_secret' : environment.get_cookie_secret(), 
    'static_path' : environment.get_local_position('static'),
    'template_path' : environment.get_local_position('template'),
    'ui_modules' : {
        'List' : modules.ListModule,
        'SinglePage' : modules.SinglePageModule,
        'PersonIndicator' : modules.PersonIndicatorModule,
    }
    #'log_file_prefix': '8888.log',
}
