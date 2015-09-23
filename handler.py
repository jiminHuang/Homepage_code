# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月03日 星期四 21时10分36秒
#
'''
    handler 处理业务逻辑
'''
import tornado.web
import database
import datetime

class BaseHandler(tornado.web.RequestHandler):
    '''
        基础handler，是其他handler的基类，将404错误即未被规则匹配的请求重定向到404网页
    '''
    def get(self):
        self.write_error(404)
    
    def write_error(self, status_code, **kwargs):
        self.render('404.html', title="404")

class SafeHandler(BaseHandler):
    '''
        handler 用来定义get_current_user方法，该方法在其他方法请求检查用户是否登陆时被调用
    '''
    def get_current_user(self):
        return self.get_secure_cookie("user_id")

class MainHandler(BaseHandler):
    '''
        首页handler
    '''
    def get(self):
        self.render("index.html", page_title="Wuhan University Internet Data Mining Labratory")

class ArticlesHandler(BaseHandler):
    '''
        文章列表页handler
    '''
    def get(self):
        self.render("articles.html", page_title=u"News - Wuhan University Internet Data Mining Laboratory")

class ArticleHandler(BaseHandler):
    '''
        文章页handler
    '''
    def get(self):
        article = {
            "article_title" : "Donec id elit non mi porta gravida at eget metus",
            "article_author" : "Min Peng", 
            "article_publish_time" : "2015-09-19 20:32", 
            "article_abstract" : "Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.",
            "article_image" : "switch_one.jpeg",
            "article_text" : "<p>nec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p><p>nec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p><p>nec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p><p>nec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p><p>nec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p><p>nec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>",
            "article_viewed" : 46,
        }
        article["article_image"] = 'img/' + article["article_image"]
        self.render(
            "article.html", 
            page_title=article["article_title"], 
            article=article,
        )

class PersonHandler(BaseHandler):
    '''
        人物页handler
    '''
    def get(self, username):
        person = database.User.get(username=username)
        person.image = 'img/' + person.user_id + '.jpeg'
        
        backgrounds = database.Background.query(person.user_id)
        for background in backgrounds:
            background.start_time=\
                background.start_time.strftime("%m/%Y")
            background.end_time=\
                background.end_time.strftime("%m/%Y")
        person.backgrounds = backgrounds
        self.render(
            "person.html", 
            page_title=\
                username\
                    +"- Wuhan University Internet Data Mining Laboratory",
            person=person,
        )
