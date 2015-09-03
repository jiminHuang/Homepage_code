# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月03日 星期四 14时19分22秒
#

'''
    启动Tornado服务器的入口
'''

import tornado.ioloop
import tornado.autoreload
import application
from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.application.listen(options.port)
    server_instance = tornado.ioloop.IOLoop.instance()
    #tornado.autoreload.add_reload_hook(database.release)
    server_instance.start()
    
