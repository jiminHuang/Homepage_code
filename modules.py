# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月16日 星期三 20时36分43秒
#
'''
    包含前端模块定义的文件
'''
import tornado.web

class ListModule(tornado.web.UIModule):
    def render(self):
        return ''
    
    def css_files(self):
        return "/static/css/list.css"
