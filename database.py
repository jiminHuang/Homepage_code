# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月22日 星期二 21时40分29秒
#
'''
    数据层文件
    包括持久化和操作
'''

import torndb
import config
import logging
import hashlib
import chewer


def get_connection(function):
    '''
        装饰器 获取数据库连接函数
    '''
    def wrapper(cls, *args, **kwargs):
        try:
            connection =\
                torndb.Connection(
                    ":".join(
                        [
                            config.Config.MYSQL_ADDRESS,
                            config.Config.MYSQL_PORT
                        ]
                    ),
                    cls.db,
                    config.Config.MYSQL_USER,
                    config.Config.MYSQL_PASSWD,
                )
        except AttributeError:
            logging.error(
                (
                    'Mysql Connection Error: '
                    'class {cls} db not assigned'
                ).format(
                    cls=cls.__name__
                )
            )
            return None if 'query' not in function.__name__ else []
        return function(cls, connection, *args, **kwargs)

    return wrapper


class TypeList(list):
    '''
        扩展list对象 捕获异常
    '''

    def __getitem__(self, index):
        '''
            改写默认getitem方法，索引减1并捕获异常
        '''
        try:
            return super(TypeList, self).__getitem__(index - 1)
        except IndexError:
            logging.error('Typelist GetItem Error')
            logging.error('Error List: {error_list}'.format(error_list=self))
            logging.error(
                'Error Index: {error_index}'.format(
                    error_index=index
                )
            )
            return 'Unknown'

    def index(self, attr):
        '''
            改写默认index方法，索引加1并抛出异常
        '''
        return super(TypeList, self).index(attr) + 1


class User(object):
    '''
        user表持久化
    '''
    db = 'homepage'
    USER_TYPE = TypeList(
        [
            u'Mentor',
            u'Doctor',
            u'Graduate',
            u'UnderGraduate',
            u'Visitor'
        ]
    )

    @classmethod
    @get_connection
    def get_in_user_id(cls, connection, user_id):
        '''
            获取一个user信息
        '''
        sql = 'SELECT * FROM user WHERE user_id = %s'

        return connection.get(sql, user_id)

    @classmethod
    @get_connection
    def get_in_username(cls, connection, username):
        '''
            获取一个user信息
        '''
        sql = 'SELECT * FROM user WHERE username = %s'

        return connection.get(sql, username)

    @classmethod
    @get_connection
    def query(cls, connection, request_type=None):
        '''
            首页 user列表 query方法
        '''
        sql = 'SELECT * FROM user '
        where_clause =\
            (
                'WHERE type != {visitor_type} '
                'ORDER BY type'
            ).format(visitor_type=User.USER_TYPE.index("Visitor"))\
            if request_type is None\
            else 'WHERE type = {request_type}'.format(
                request_type=request_type,
            )

        return connection.query(sql + where_clause)

    @classmethod
    @get_connection
    def query_in_project(cls, connection, project_id):
        '''
            获取project_id相关user
        '''
        sql =\
            (
                'SELECT * '
                'FROM user_project '
                'NATURAL JOIN user '
                'WHERE project_id = {project_id} '
                'ORDER BY role'
            ).format(project_id=project_id)

        return connection.query(sql)

    @classmethod
    def chew(cls, user):
        user.image = chewer.static_image('person/' + user.user_id)
        user.english_name =\
            ''.join((
                user.firstname.capitalize(),
                ' ',
                user.lastname.capitalize(),
            ))
        user.type = User.USER_TYPE[int(user.type)]

        return user


class Background(object):
    '''
        用户学历背景 background表持久化对象
    '''
    db = 'homepage'
    BACKGROUND_TYPE = TypeList(['Bachelor', 'Master', 'Ph.D'])

    @classmethod
    @get_connection
    def query(cls, connection, user_id):
        '''
            根据user_id 获取对应user背景
        '''
        sql = (
            'SELECT * '
            'FROM user_background '
            'NATURAL JOIN background '
            'WHERE user_id = %s '
            'ORDER BY background_type'
        )

        return connection.query(sql, user_id)

    @classmethod
    def chew(cls, background):
        '''
            background 处理函数
        '''
        background.background_type =\
            cls.BACKGROUND_TYPE[background.background_type]
        background.start_time =\
            chewer.strftime_present("%m/%Y", background.start_time)
        background.end_time =\
            chewer.strftime_present("%m/%Y", background.end_time)

        return background


class Experience(object):
    '''
        工作经历 experience持久化对象
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def query(cls, connection, user_id):
        '''
            根据user_id获取对应experience
        '''
        sql =\
            (
                'SELECT * '
                'FROM user_experience '
                'NATURAL JOIN experience '
                'WHERE user_id = %s'
            )

        return connection.query(sql, user_id)

    @classmethod
    def chew(cls, experience):
        '''
            experience 后续处理方法
        '''
        experience.start_time =\
            chewer.strftime_present("%m/%Y", experience.start_time)
        experience.end_time =\
            chewer.strftime_present("%m/%Y", experience.end_time)

        return experience


class Interests(object):
    '''
        研究方向 interests持久化对象
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def query(cls, connection, user_id):
        '''
            根据user_id获取对应interests
        '''
        sql =\
            (
                'SELECT * '
                'FROM user_interests '
                'NATURAL JOIN interests '
                'WHERE user_id = %s'
            )

        return connection.query(sql, user_id)


class Article(object):
    '''
        文章 article 持久化对象
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def get(cls, connection, article_id):
        '''
            根据article_id获取对应文章信息
        '''
        sql =\
            (
                'SELECT * '
                'FROM article '
                'WHERE article_id = %s'
            )

        return connection.get(sql, article_id)

    @classmethod
    @get_connection
    def query(cls, connection, query_num=1):
        query_num = query_num if query_num >= 1 else 1

        sql =\
            (
                'SELECT * '
                'FROM article '
                'WHERE type = 1 '
                'ORDER BY publish_time DESC '
                'LIMIT {start_num}, {end_num}'
            ).format(
                start_num=(query_num - 1) * 10,
                end_num=query_num * 10,
            )

        return connection.query(sql)

    @classmethod
    def author(cls, author):
        author = author.strip()
        user = User.get_in_user_id(author)
        return User.chew(user) if user is not None else author

    @classmethod
    def authors(cls, author):
        # author正常输入
        return [cls.author(user) for user in author.split(',')]

    @classmethod
    def chew(cls, article):
        article.article_image = chewer.static_image(article.article_id)
        article.author = Article.authors(article.author)
        article.short_abstract = chewer.text_cutter(article.abstract, 255)

        return article


class Publisher(object):
    '''
        出版 Publisher表持久化对象
    '''
    db = 'homepage'
    PUBLISHER_TYPE = TypeList(['Journal', 'Conference'])

    @classmethod
    @get_connection
    def get(cls, connection, publisher_id):
        '''
            publisher get方法
        '''
        sql =\
            (
                'SELECT * '
                'FROM publisher '
                'WHERE publisher_id = {publisher_id}'
            ).format(publisher_id=publisher_id)

        return connection.get(sql)

    @classmethod
    def chew(cls, publisher):
        '''
            publisher 处理方法
        '''
        publisher.publisher_type = cls.PUBLISHER_TYPE[publisher.publisher_type]
        return publisher


class Paper(object):
    '''
        论文 Paper表持久化对象
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def get(cls, connection, article_id):
        '''
            paper get方法
        '''
        sql =\
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'WHERE article_id = %s'
            )
        return connection.get(sql, article_id)

    @classmethod
    @get_connection
    def query(cls, connection, query_num=1):
        '''
            paper query方法
        '''

        query_num = query_num if query_num >= 1 else 1

        sql =\
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'WHERE article.type = 2 '
                'ORDER BY publish_year DESC '
                'LIMIT {query_start}, {query_end}'
            ).format(
                query_start=(query_num - 1) * 10,
                query_end=10,
            )
        return connection.query(sql)

    @classmethod
    @get_connection
    def query_in_year(cls, connection, year):
        year = year + '-01-01'

        sql =\
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'WHERE publish_year = %s'
            )

        return connection.query(sql, year)

    @classmethod
    @get_connection
    def query_in_user(cls, connection, user_id):
        # 构建模糊查询表达式
        user_id =\
            ''.join((
                '%',
                str(user_id),
                '%',
            ))

        sql = (
            'SELECT * '
            'FROM article '
            'NATURAL JOIN paper '
            'WHERE type = 2 '
            'AND author LIKE %s '
            'ORDER BY publish_year DESC'
        )

        return connection.query(sql, user_id)

    @classmethod
    def chew(cls, paper):
        paper.publisher = Publisher.chew(Publisher.get(paper.publisher_id))

        if paper.in_press is not None:
            paper.title += '(In Press)'

        paper.publish_year =\
            chewer.strftime_present("%Y", paper.publish_year)

        paper = Article.chew(paper)

        if paper.paper_url is None:
            paper.pdf_url =\
                ''.join(
                    (
                        'paper/',
                        paper.article_id,
                        '.pdf',
                    )
                )

        return paper

    @classmethod
    @get_connection
    def insert(cls, connection, **kwargs):
        '''
            论文插入方法
        '''
        request_values = [
            'title',
            'author',
            'abstract',
            'publisher_id',
            'start_page',
            'end_page',
            'publish_year',
        ]

        for value in request_values:
            if kwargs.get(value, None) is None:
                return False

        article_id = hashlib.md5(kwargs['title']).hexdigest()

        sql =\
            (
                'INSERT INTO article '
                'VALUE('
                '%s, %s, now(), null, null, null, %s, 2, 0, %s)'
            )

        try:
            connection.execute(
                sql,
                article_id,
                kwargs['author'],
                kwargs['abstract'],
                kwargs['title'],
            )
        except Exception, e:
            logging.error('paper insert error in article: ' + str(e))
            return False

        if kwargs.get('volume', None) is None:
            kwargs['volume'] = 'null'

        if kwargs.get('number', None) is None:
            kwargs['number'] = 'null'

        sql =\
            (
                'INSERT INTO paper '
                'VALUE(%s, '
                '{publisher_id}, '
                '{volume}, '
                '{number}, '
                '{start_page}, '
                '{end_page}, %s, %s)'
            ).format(
                publisher_id=kwargs['publisher_id'],
                volume=kwargs['volume'],
                number=kwargs['number'],
                start_page=kwargs['start_page'],
                end_page=kwargs['end_page'],
            )
        try:
            connection.execute(
                sql,
                article_id,
                kwargs['publish_year'],
                kwargs.get('paper_url', None),
            )
        except Exception, e:
            logging.error('paper insert error in paper: ' + str(e))
            return False

        return True


class Item(object):
    '''
        项目类型 item表持久化对象
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def query(cls, connection, project_id):
        sql =\
            (
                'SELECT * '
                'FROM project_item '
                'NATURAL JOIN item '
                'WHERE project_id = {project_id}'
            ).format(project_id=project_id)

        return connection.query(sql)


class Project(object):
    '''
        项目 project表持久化对象
    '''
    db = 'homepage'
    PROJECT_TYPE = TypeList(['academic', 'application'])

    @classmethod
    @get_connection
    def get(cls, connection, project_id):
        '''
            获取对应project_id的项目信息
        '''
        sql =\
            (
                'SELECT * '
                'FROM project '
                'WHERE project_id = {project_id}'
            ).format(project_id=project_id)
        return connection.get(sql)

    @classmethod
    @get_connection
    def query(cls, connection, query_num=1):
        '''
            获取10数量的project信息
        '''

        query_num = query_num if query_num >= 1 else 1

        sql =\
            (
                'SELECT * '
                'FROM project '
                'ORDER BY start_time DESC '
                'LIMIT {start_num}, {end_num}'
            ).format(
                start_num=(query_num - 1) * 10,
                end_num=10,
            )
        return connection.query(sql)

    @classmethod
    @get_connection
    def query_in_year(cls, connection, year):
        '''
            得到年份相关projects
        '''
        sql =\
            (
                'SELECT * '
                'FROM project '
                'WHERE end_time >= %s '
                'ORDER BY start_time DESC '
            )

        start_time = year + '-01-01'
        return connection.query(sql, start_time)

    @classmethod
    @get_connection
    def query_in_user(cls, connection, user_id):
        '''
            得到与user_id相关的全部projects
        '''
        sql =\
            (
                'SELECT * '
                'FROM user_project '
                'NATURAL JOIN project '
                'WHERE user_id = %s '
                'ORDER BY start_time DESC'
            )
        return connection.query(sql, user_id)

    @classmethod
    def chew(cls, project):
        project.item = Item.query(project.project_id)

        project.users = User.query_in_project(project.project_id)
        project.users = [User.chew(user) for user in project.users]
        project.project_image =\
            chewer.static_image(
                'project/' + str(project.project_id)
            )

        project.start_time =\
            chewer.strftime_present("%m/%Y", project.start_time)

        project.end_time =\
            chewer.strftime_present("%m/%Y", project.end_time)
        return project


class Prize(object):
    '''
        奖项 prize持久化对象
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def query_in_user(cls, connection, user_id):
        '''
            根据user_id得到对应奖项
        '''
        sql =\
            (
                'SELECT * '
                'FROM user_prize '
                'NATURAL JOIN prize '
                'WHERE user_id = %s '
                'ORDER BY prize_year DESC'
            )

        return connection.query(sql, user_id)

    @classmethod
    def chew(cls, prize):
        prize.prize_year =\
            chewer.strftime_present("%Y", prize.prize_year)
        if not prize.prize_facility:
            prize.prize_facility = ''

        return prize


class Proprietary(object):
    '''
        专利或软著 proprietary持久化对象
    '''
    db = 'homepage'
    PROPRIETARY_TYPE = TypeList(
        [
            'National Invention Patents(CHINA)',
            'National Software Copyright(CHINA)'
        ]
    )

    @classmethod
    @get_connection
    def query_in_user(cls, connection, user_id):
        '''
            根据user_id得到对应奖项
        '''
        sql =\
            (
                'SELECT * '
                'FROM user_proprietary '
                'NATURAL JOIN proprietary '
                'WHERE user_id = %s '
                'ORDER BY proprietary_time DESC'
            )

        return connection.query(sql, user_id)

    @classmethod
    def chew(cls, proprietary):
        '''
            proprietary 后续处理方法
        '''
        proprietary.proprietary_time =\
            chewer.strftime_present("%Y", proprietary.proprietary_time)
        return proprietary


class Model(object):
    '''
        model表持久化
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def get_in_model_id(cls, connection, model_id):
        '''
            按model_id取单条记录
        '''
        sql = \
            (
                'SELECT * FROM model WHERE model_id = %s'
            )
        return connection.get(sql, model_id)

    @classmethod
    @get_connection
    def get_in_refer(cls, connection, refer):
        '''
            按所属论文id取单条记录（一一对应）
        '''
        sql = \
            (
                'SELECT * FROM model WHERE refer = %s'
            )
        return connection.get(sql, refer)

    @classmethod
    @get_connection
    def query(cls, connection, query_num=1):
        '''
            直接返回全部model记录
            query_num表示显示次数，即第几次显示
        '''
        entry_number = 10  # 每次显示的记录数目
        query_num = query_num if query_num >= 1 else 1

        sql = (
            'SELECT * FROM model LIMIT {start}, {end}'
        ).format(
            start=(query_num - 1) * entry_number,
            end=query_num * entry_number,
        )

        return connection.query(sql)

    @classmethod
    @get_connection
    def query_in_time_order(cls, connection, query_num=1):
        '''
            按照所属论文的发表时间进行排序返回记录集
        '''
        entry_number = 10  # 每次显示的记录数目
        query_num = query_num if query_num >= 1 else 1

        sql = (
            'SELECT * '
            'FROM paper '
            'NATURAL JOIN model '
            'ORDER BY publish_year DESC'
            'LIMIT {start}, {end}'
        ).format(
            start=(query_num - 1) * entry_number,
            end=query_num * entry_number,
        )
        return connection.query(sql)

    @classmethod
    def chew(cls, model):
        '''
            model 处理函数
        '''
        application = Application.get_in_app_id(model.app)
        if application:
            model.app = application.app_type
        else:
            model.app = 'Not Classified Yet'

        return model


class Application(object):
    '''
        模型所属类别 application表持久化
    '''
    db = 'homepage'
    # APPLICATION_TYPE = ['', '', '']

    @classmethod
    @get_connection
    def get_in_app_id(cls, connection, app_id):
        '''
            按app_id取类别记录
        '''
        sql = 'SELECT * FROM model_application WHERE app_id = %s'
        return connection.get(sql, app_id)

    @classmethod
    def chew(cls, application):
        '''
            application 处理函数
        '''

        return application


class Baseline(object):
    '''
        baseline表持久化
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def get_in_base_id(cls, connection, base_id):
        '''
            按base_id获取单条记录
        '''
        sql = 'SELECT * FROM model_baseline WHERE base_id = %s'
        return connection.get(sql, base_id)

    @classmethod
    @get_connection
    def query(cls, connection, exp_id):
        '''
            按exp_id所属实验获取属于该实验的baseline记录
        '''
        sql = 'SELECT * FROM model_baseline WHERE exp_id = %s'
        return connection.query(sql, exp_id)

    @classmethod
    def chew(cls, baseline):
        '''
            baseline 处理函数
        '''

        return baseline


class Dataset(object):
    '''
        dataset表持久化
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def get_in_data_id(cls, connection, data_id):
        '''
            按data_id取单条记录
        '''
        sql = 'SELECT * FROM model_dataset WHERE data_id = %s'
        return connection.get(sql, data_id)

    @classmethod
    @get_connection
    def query_in_model_id(cls, connection, model_id):
        '''
            按model_id所属模型获取属于该模型的dataset记录
        '''
        sql = 'SELECT * FROM model_dataset WHERE model_id = %s'
        return connection.query(sql, model_id)

    @classmethod
    @get_connection
    def query_in_exp_id(cls, connection, exp_id):
        '''
            按exp_id所属实验获取属于该实验的dataset记录
        '''
        sql = 'SELECT * FROM model_dataset WHERE exp_id = %s'
        return connection.query(sql, exp_id)

    @classmethod
    def chew(cls, dataset):
        '''
            dataset 处理函数
        '''

        return dataset


class Evaluation(object):
    '''
        评估信息evaluation表持久化
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def get_in_evl_id(cls, connection, evl_id):
        '''
            按evl_id取单条记录
        '''
        sql = 'SELECT * FROM model_evaluation WHERE evl_id = %s'
        return connection.get(sql, evl_id)

    @classmethod
    @get_connection
    def query(cls, connection, exp_id):
        '''
            按exp_id所属实验获取属于该实验的evaluation记录
        '''
        sql = 'SELECT * FROM model_evaluation WHERE exp_id = %s'
        return connection.query(sql, exp_id)

    @classmethod
    def chew(cls, evaluation):
        '''
            evaluation 处理函数
        '''

        return evaluation


class Result(object):
    '''
        实验结果信息result表持久化
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def get_in_result_id(cls, connection, result_id):
        '''
            按result_id取单条记录
        '''
        sql = 'SELECT * FROM model_result WHERE result_id = %s'
        return connection.get(sql, result_id)

    @classmethod
    @get_connection
    def query(cls, connection, exp_id):
        '''
            按exp_id所属实验获取属于该实验的result记录
        '''
        sql = 'SELECT * FROM model_result WHERE exp_id = %s'
        return connection.query(sql, exp_id)

    @classmethod
    def chew(cls, result):
        '''
            result 处理函数
        '''
        result.result_pic = \
            chewer.static_image('result/' + str(result.result_id))

        return result


class Experiment(object):
    '''
        experiment表持久化
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def get_in_exp_id(cls, connection, exp_id):
        '''
            按exp_id取单条记录
        '''
        sql = 'SELECT * FROM model_experiment WHERE exp_id = %s'
        return connection.get(sql, exp_id)

    @classmethod
    @get_connection
    def query(cls, connection, model_id):
        '''
            按model_id所属模型获取属于该模型的实验记录，一条或多条
        '''
        sql = 'SELECT * FROM model_experiment WHERE model_id = %s'
        return connection.query(sql, model_id)

    @classmethod
    def chew(cls, experiment):
        '''
            experiment 处理函数
        '''

        return experiment


class Process(object):
    '''
        模型详细信息process表持久化
    '''
    db = 'homepage'

    @classmethod
    @get_connection
    def get_in_proc_id(cls, connection, proc_id):
        '''
            按proc_id取单条记录
        '''
        sql = 'SELECT * FROM model_process WHERE proc_id = %s'
        return connection.get(sql, proc_id)

    @classmethod
    def chew(cls, process):
        '''
            process 处理函数
        '''
        if process.proc_pic:
            process.proc_pic = \
                chewer.static_image('process/' + str(process.proc_id))
        else:
            process.proc_pic = ''

        return process
