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
import logging
import datetime
import traceback
import email_sender
from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.application.listen(options.port)
    server_instance = tornado.ioloop.IOLoop.instance()
    # tornado.autoreload.add_reload_hook(database.release)
    try:
        server_instance.start()
    except KeyboardInterrupt:
        logging.error("Existing")
        exit_error = '按键Cc退出'
    except Exception, e:
        logging.exception(e)
        exit_error = traceback.format_exec()
    finally:
        server_instance.add_callback(server_instance.stop)
        exit_error = str(datetime.datetime.now()) + '\n' + exit_error
        email_sender.send(title='服务器退出错误', message=exit_error)
