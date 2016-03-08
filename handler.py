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
import chewer
import email_sender
import traceback


class BaseHandler(tornado.web.RequestHandler):
    '''
        基础handler，是其他handler的基类，将404错误即未被规则匹配的请求重定向到404网页
    '''

    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        try:
            message = \
                '\n'.join(traceback.format_exception(*kwargs['exc_info']))
        except KeyError:
            message = str(status_code)
        email_sender.async_send(title="服务器错误", message=message)
        self.render('404.html', page_title="404")


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
        if articles:
            articles = [database.Article.chew(article) for article in articles]

        this_year = chewer.this_year()

        papers = database.Paper.query_in_year(this_year)
        if papers:
            papers = [database.Paper.chew(paper) for paper in papers]

        projects = database.Project.query_in_year(str(int(this_year) - 2))
        if projects:
            projects = [database.Project.chew(project) for project in projects]

        persons = database.User.query()
        persons = [database.User.chew(person) for person in persons]
        user_types = database.User.USER_TYPE[:4]

        self.render(
            "index.html",
            page_title="Wuhan University Internet Data Mining Labratory",
            articles=articles,
            papers=papers,
            projects=projects,
            persons=persons,
            user_types=user_types,
        )


class ArticlesHandler(BaseHandler):
    '''
        文章列表页handler
    '''

    def get(self):
        articles = database.Article.query()
        if articles:
            articles = [database.Article.chew(article) for article in articles]
        self.render(
            "articles.html",
            page_title=u"News - WUIDML",
            articles=articles,
        )

    def post(self):
        query_num = self.get_argument('query_num', None)

        if query_num is None:
            self.write('failed')
            return None

        articles = database.Article.query(int(query_num))

        write_str =\
            ''.join(
                (
                    self.render_string(
                        'module/articleItem.html',
                        article=database.Article.chew(article),
                    ) for article in articles
                )
            )

        load_more = '-1' if len(articles) < 10 else str(int(query_num) + 1)

        self.write({'write_str': write_str, 'load_more': load_more})


class ArticleHandler(BaseHandler):
    '''
        文章页handler
    '''

    def get(self, article_id):
        # article
        article = database.Article.get(article_id)

        article = database.Article.chew(article)

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
        # person 基本信息
        person = database.User.get_in_username(username)
        person = database.User.chew(person)

        # person 教育背景
        person.backgrounds =\
            [
                database.Background.chew(background)
                for background in database.Background.query(person.user_id)
            ]

        # person 工作经历
        person.experiences =\
            [
                database.Experience.chew(experience)
                for experience in database.Experience.query(person.user_id)
            ]

        # person 研究方向
        interests = database.Interests.query(person.user_id)
        person.interests = interests

        # person 论文
        papers = database.Paper.query_in_user(person.user_id)
        person.papers = [database.Paper.chew(paper) for paper in papers]

        # person 项目
        person.projects =\
            [
                database.Project.chew(project)
                for project in database.Project.query_in_user(person.user_id)
            ]

        # person 奖项
        person.prizes =\
            [
                database.Prize.chew(prize)
                for prize in database.Prize.query_in_user(person.user_id)
            ]

        # person 专利/软著
        person.proprietaries =\
            [
                database.Proprietary.chew(proprietary)
                for proprietary in database.Proprietary.query_in_user(
                    person.user_id
                )
            ]

        self.render(
            "person.html",
            page_title=username
            + "- Wuhan University Internet Data Mining Laboratory",
            person=person,
            publisher_type=database.Publisher.PUBLISHER_TYPE,
            proprietary_type=database.Proprietary.PROPRIETARY_TYPE,
        )


class PaperHandler(BaseHandler):
    '''
        论文页handler
    '''

    def get(self, article_id):
        paper = database.Paper.get(article_id)

        paper = database.Paper.chew(paper)

        model = database.Model.get_in_refer(paper.article_id)

        self.render(
            "paper.html",
            page_title=paper.title,
            paper=paper,
            model=model,
        )


class ResearchHandler(BaseHandler):
    '''
        Research页 handler
    '''

    def get(self):
        papers = database.Paper.query()

        papers = [database.Paper.chew(paper) for paper in papers]

        self.render(
            "research.html",
            page_title="Research-WUIDML",
            papers=papers,
        )

    def post(self):
        query_num = self.get_argument('query_num', None)

        if query_num is None:
            self.write('failed')
            return None

        papers = database.Paper.query(int(query_num))

        write_str =\
            ''.join(
                (
                    self.render_string(
                        'module/researchItem.html',
                        paper=database.Paper.chew(paper),
                    ) for paper in papers
                )
            )

        load_more = '-1' if len(papers) < 10 else str(int(query_num) + 1)

        self.write({'write_str': write_str, 'load_more': load_more})


class ProjectHandler(BaseHandler):
    '''
        项目页handler
    '''

    def get(self, project_id):
        project = database.Project.get(project_id)

        project = database.Project.chew(project)

        self.render(
            "project.html",
            page_title=project.project_name + "-WUIDML",
            project=project,
        )


class ProjectsHandler(BaseHandler):
    '''
        项目列表页handler
    '''

    def get(self):
        projects = database.Project.query()

        if projects:
            projects = [database.Project.chew(project) for project in projects]

        self.render(
            "projects.html",
            page_title="Projects-WUIDML",
            projects=projects,
        )

    def post(self):
        query_num = self.get_argument('query_num', None)

        if query_num is None:
            self.write('failed')
            return None

        projects = database.Project.query(int(query_num))

        write_str =\
            ''.join(
                (
                    self.render_string(
                        'module/projectItem.html',
                        project=database.Project.chew(project),
                    ) for project in projects
                )
            )

        load_more = '-1' if len(projects) < 10 else str(int(query_num) + 1)

        self.write({'write_str': write_str, 'load_more': load_more})


class ModelsHandler(BaseHandler):
    '''
        模型列表页面handler
    '''

    def get(self):
        models = database.Model.query()
        if models:
            models = [database.Model.chew(model) for model in models]
        self.render(
            "models.html",
            page_title="Models-WUIDML",
            models=models,
        )

    def post(self):
        query_num = self.get_argument('query_num', None)

        if query_num is None:
            self.write('failed')
            return None

        models = database.Model.query(int(query_num))

        write_str =\
            ''.join(
                (
                    self.render_string(
                        'module/modelItem.html',
                        model=database.Model.chew(model),
                    ) for model in models
                )
            )

        load_more = '-1' if len(models) < 10 else str(int(query_num) + 1)

        self.write({'write_str': write_str, 'load_more': load_more})


class ModelHandler(BaseHandler):
    '''
        模型展示页handler
    '''
    def get(self, model_id):

        model = database.Model.get_in_model_id(model_id)
        model = database.Model.chew(model)

        paper = database.Paper.get(model.refer)
        paper = database.Paper.chew(paper)

        process = database.Process.get_in_proc_id(model.proc)
        process = database.Process.chew(process)

        experiments = database.Experiment.query(model_id)
        if experiments:
            experiments = (
                [database.Experiment.chew(experiment)
                    for experiment in experiments]
            )

        self.render(
            "model.html",
            page_title=model.name,
            model=model,
            paper=paper,
            process=process,
            experiments=experiments,
        )


class ExperimentHandler(BaseHandler):
    '''
        单个模型实验效果展示页handler
    '''
    def get(self, exp_id):

        model_id = self.get_argument("model_id", 0)

        experiment = database.Experiment.get_in_exp_id(exp_id)
        experiment = database.Experiment.chew(experiment)

        model = database.Model.get_in_model_id(model_id)
        model = database.Model.chew(model)

        datasets = database.Dataset.query_in_model_id(model_id)
        if not datasets:  # 若按照model_id取出来记录为空，则说明用exp_id标注
            datasets = database.Dataset.query_in_exp_id(exp_id)
        if datasets:
            datasets = (
                [database.Dataset.chew(dataset)
                    for dataset in datasets]
            )

        evaluations = database.Evaluation.query(exp_id)
        if evaluations:
            evaluations = (
                [database.Evaluation.chew(evaluation)
                    for evaluation in evaluations]
            )

        baselines = database.Baseline.query(exp_id)
        if baselines:
            baselines = (
                [database.Baseline.chew(baseline)
                    for baseline in baselines]
            )

        results = database.Result.query(exp_id)
        if results:
            results = (
                [database.Result.chew(result)
                    for result in results]
            )

        self.render(
            "experiment.html",
            page_title=experiment.exp_name,
            experiment=experiment,
            datasets=datasets,
            evaluations=evaluations,
            baselines=baselines,
            results=results,
            model=model,
        )

    def post(self):
        '''
            接收客户请求做出相应显示
        '''
