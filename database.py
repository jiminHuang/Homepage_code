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


def none_input_catcher(function):
    '''
        捕获空输入
    '''
    logging_str =\
        'None Input Catched: function {function}'.format(
            function=function.__name__
        )

    def wrapper(*args, **kwargs):
        def check_arg(arg):
            '''
                检查参数是否为None
            '''
            if arg is None:
                raise TypeError

        try:
            map(check_arg, args)
            map(check_arg, kwargs.values())
            return function(*args, **kwargs)
        except TypeError, e:
            logging.error(logging_str)
            logging.info(e)
            return None

    return wrapper


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
    @none_input_catcher
    @get_connection
    def get_in_user_id(cls, connection, user_id):
        '''
            获取一个user信息
        '''
        sql = 'SELECT * FROM user WHERE user_id = %s'

        return connection.get(sql, user_id)

    @classmethod
    @none_input_catcher
    @get_connection
    def get_in_username(cls, connection, username):
        '''
            获取一个user信息
        '''
        sql = 'SELECT * FROM user WHERE username = %s'

        return connection.get(sql, username)

    @classmethod
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
    def author(cls, author):
        author = author.strip()
        user = User.get_in_user_id(author)
        return User.chew(user) if user is not None else author

    @classmethod
    @none_input_catcher
    def authors(cls, author):
        # author正常输入
        return [cls.author(user) for user in author.split(',')]

    @classmethod
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
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
    @none_input_catcher
    def chew(cls, proprietary):
        '''
            proprietary 后续处理方法
        '''
        proprietary.proprietary_time =\
            chewer.strftime_present("%Y", proprietary.proprietary_time)
        return proprietary
