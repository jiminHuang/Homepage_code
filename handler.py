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
import timechewer

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
        articles = database.Article.query()
        for article in articles:
            article.article_image = 'img/' + article.article_id + '.jpeg'
        self.render(
            "articles.html",
            page_title=u"News - Wuhan University Internet Data Mining Laboratory",
            articles=articles,
        )

class ArticleHandler(BaseHandler):
    '''
        文章页handler
    '''
    def get(self, article_id):
        #article 
        article = database.Article.get(article_id)
        if article is None:
            self.write_error("404")
        article.article_image = 'img/' + article.article_id + '.jpeg'
        
        self.render(
            "article.html", 
            page_title=article.title, 
            article=article,
        )

class PersonHandler(BaseHandler):
    '''
        人物页handler
    '''
    def get(self, username):
        #person 基本信息
        person = database.User.get(username=username)
        person.image = 'img/' + person.user_id + '.jpeg'
        
        #person 教育背景
        backgrounds = database.Background.query(person.user_id)
        if backgrounds is not None:
            for background in backgrounds:
                background.start_time=\
                    timechewer.strftime_present("%m/%Y", background.start_time)
                background.end_time=\
                    timechewer.strftime_present("%m/%Y", background.end_time)
        person.backgrounds = backgrounds
    
        #person 工作经历
        experiences = database.Experience.query(person.user_id)
        if experiences is not None:
            for experience in experiences:
                experience.start_time=\
                    timechewer.strftime_present("%m/%Y", experience.start_time)
                experience.end_time=\
                    timechewer.strftime_present("%m/%Y", experience.end_time)
        person.experiences = experiences
    
        #person 研究方向
        interests = database.Interests.query(person.user_id)
        person.interests = interests

        self.render(
            "person.html", 
            page_title=\
                username\
                    +"- Wuhan University Internet Data Mining Laboratory",
            person=person,
        )

class PaperHandler(BaseHandler):
    '''
        论文页handler
    '''
    def get(self, article_id):
        paper = database.Paper.get(article_id)
        paper.publish_year = timechewer.strftime_present("%Y", paper.publish_year)
        if paper.paper_url is None:
            paper.pdf_available = True
            paper.paper_url =\
                ''.join(
                    'paper/',
                    paper.article_id,
                    '.pdf',    
                )
        else:
            paper.pdf_available = False

        self.render(
            "paper.html",
            page_title=paper.title,
            paper=paper,
        )
