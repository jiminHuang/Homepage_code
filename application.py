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
    (r"/research", handler.ResearchHandler),
    (r"/projects", handler.ProjectsHandler),
    (r"/article/(\S+)", handler.ArticleHandler),
    (r"/person/(\w+)", handler.PersonHandler),
    (r"/paper/(\S+)", handler.PaperHandler),
    (r"/project/(\d+)", handler.ProjectHandler),
    (r"/models", handler.ModelsHandler),
    (r"/model/(\S+)", handler.ModelHandler),
    (r"/experiment/(\S+)", handler.ExperimentHandler),
    (r".*", handler.BaseHandler),
], **settings)
