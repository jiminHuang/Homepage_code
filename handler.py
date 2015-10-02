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
import imagechewer

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
        articles = database.Article.query()
        for article in articles:
            article.article_image = imagechewer.static_image(article.article_id)
            article.abstract = article.abstract[:255] + '...'
        
        papers = database.Paper.query()
        if papers:
            papers = papers[:3] 
            for paper in papers:
                paper.publish_year = timechewer.strftime_present("%Y", paper.publish_year)
                paper.author =\
                    [
                        database.Article.author(author)
                            for author in paper.author.split(",")
                    ]
        
        projects = database.Project.query()
        if projects:
            projects = projects[:4]
            for project in projects:
                project.project_image = imagechewer.static_image(project.project_id)

                project.start_time =\
                    timechewer.strftime_present("%m/%Y", project.start_time)

                project.end_time =\
                    timechewer.strftime_present("%m/%Y", project.end_time)
        
        persons = database.User.query()
        for person in persons:
            person.image = imagechewer.static_image(person.user_id)

        self.render(
            "index.html",
            page_title="Wuhan University Internet Data Mining Labratory",
            articles=articles,    
            papers=papers,
            projects=projects,
            persons=persons,
        )

class ArticlesHandler(BaseHandler):
    '''
        文章列表页handler
    '''
    def get(self):
        articles = database.Article.query()
        for article in articles:
            article.article_image = imagechewer.static_image(article.article_id)
            article.author =\
                [
                    database.Article.author(author)\
                        for author in article.author.split(",")
                ]
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
        article.article_image = imagechewer.static_image(article.article_id)
        article.author =\
            [
                database.Article.author(author)\
                    for author in article.author.split(",")
            ]
        
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
        if person is None:
            self.write_error("404")
        person.image = imagechewer.static_image(person.user_id)
        
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
        
        #person 论文
        papers = database.Paper.query_in_user(person.user_id)
        for paper in papers:
            paper.publish_year = timechewer.strftime_present("%Y", paper.publish_year)
            paper.author =\
                [
                    database.Article.author(author)
                        for author in paper.author.split(",")
                ]
        person.papers = papers
        
        #person 项目
        projects = database.Projects.query_in_user(person.user_id)
        for project in projects:
            project.start_time =\
                timechewer.strftime_present("%m/%Y", project.start_time)

            project.end_time =\
                timechewer.strftime_present("%m/%Y", project.end_time)
        person.projects = projects

        self.render(
            "person.html", 
            page_title=\
                username\
                    +"- Wuhan University Internet Data Mining Laboratory",
            person=person,
            publisher_type=database.Publisher.PUBLISHER_TYPE,
        )

class PaperHandler(BaseHandler):
    '''
        论文页handler
    '''
    def get(self, article_id):
        paper = database.Paper.get(article_id)
        if paper is None:
            self.write_error(404)

        paper.images = database.PaperImage.query(article_id)
        if paper.images:
            paper.images =\
                [
                    imagechewer.static_image('paper/' + str(image.image_id), image.suffix)
                        for image in paper.images
                ]
        
        paper.publish_year = timechewer.strftime_present("%Y", paper.publish_year)
        paper.author =\
            [
                database.Article.author(author)
                    for author in paper.author.split(",")
            ]
        if paper.paper_url is None:
            paper.pdf_available = True
            paper.paper_url =\
                ''.join((
                    'paper/',
                    paper.article_id,
                    '.pdf',    
                ))
        else:
            paper.pdf_available = False

        self.render(
            "paper.html",
            page_title=paper.title,
            paper=paper,
        )

class ResearchHandler(BaseHandler):
    '''
        Research页 handler
    '''
    def get(self):
        papers = database.Paper.query()
        if not papers:
            self.write_error("404")
        for paper in papers:

            paper.publish_year =\
                timechewer.strftime_present("%Y", paper.publish_year)

            paper.author =\
                [
                    database.Article.author(author)
                        for author in paper.author.split(",")
                ]
            
            paper.abstract = paper.abstract[:255] + '...'

            paper.images = database.PaperImage.query(paper.article_id)
            if paper.images:
                paper.images =\
                    [
                        imagechewer.static_image('paper/' + str(image.image_id), image.suffix)
                            for image in paper.images
                    ]
        
        self.render(
            "research.html",
            page_title="Research-WUIDML",
            papers=papers,
        )

class ProjectHandler(BaseHandler):
    '''
        项目页handler
    '''
    
    def get(self, project_id):
        project = database.Project.get(project_id)
        
        if project is None:
            self.write_error("404")
        
        project.users = database.User.query_in_project(project_id)
        
        if not project.users:
            self.write_error("404")
        
        for user in project.users:
            user.image = imagechewer.static_image(user.user_id)

        project.start_time =\
            timechewer.strftime_present("%m/%Y", project.start_time)

        project.end_time =\
            timechewer.strftime_present("%m/%Y", project.end_time)
        
        self.render(
            "project.html",
            page_title=project.project_name+"-WUIDML",
            project=project,
        )

class ProjectsHandler(BaseHandler):
    '''
        项目列表页handler
    '''
    def get(self):
        projects = database.Project.query()
        if not projects:
            self.write_error("404")
        
        for project in projects:
            project.users = database.User.query_in_project(project.project_id)
            project.project_image = imagechewer.static_image(project.project_id)

            project.start_time =\
                timechewer.strftime_present("%m/%Y", project.start_time)

            project.end_time =\
                timechewer.strftime_present("%m/%Y", project.end_time)
        
        self.render(
            "projects.html",
            page_title="Projects-WUIDML",
            projects=projects,
        )
        
        
