# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月03日 星期四 14时24分15秒
#
'''
    加载服务器设置的application文件
'''
import tornado.web
import handler
from settings import settings

application = tornado.web.Application([
    (r"/", handler.MainHandler),
    (r"/articles", handler.ArticlesHandler),
    (r"/article/(\S+)", handler.ArticleHandler),
    (r"/person/(\w+)", handler.PersonHandler),
    (r"/paper/(\S+)", handler.PaperHandler),
    (r".*", handler.BaseHandler),
], **settings)

