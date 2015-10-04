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

def _get_connection(db):
    '''
        获取数据库连接函数
    '''
    return torndb.Connection(
        ":".join(
            [config.Config.MYSQL_ADDRESS,
            config.Config.MYSQL_PORT]
        ),
        db,
        config.Config.MYSQL_USER,
        config.Config.MYSQL_PASSWD,
    )

class TypeList(list):
    '''
        扩展list对象 捕获异常
    '''
    def __getitem__(self, index):
        '''
            改写默认getitem方法，索引减1并捕获异常
        '''
        try:
            return super(TypeList, self).__getitem__(index-1)
        except IndexError:
            logging.error('Typelist Index Error')
            logging.error('Error List: {error_list}'.format(error_list=self))
            logging.error('Error Index: {error_index}'.format(error_index=index))
            return 'Unknown'
    
class User(object):
    '''
        user表持久化
    '''
    db = 'homepage'
    USER_TYPE = TypeList([u'Mentor', u'Doctor', u'Graduate', u'UnderGraduate'])

    @classmethod
    def get(cls, user_id=None, username=None):
        '''
            获取一个user信息
        '''
        #user_id 为空
        if user_id is None and username is None:
            return None
        
        #构建数据库连接
        connection = _get_connection(cls.db)
        
        sql =  'SELECT * FROM user '
        if user_id is not None:
            sql += 'WHERE user_id = %s'
            user = user_id
        else:
            sql += 'WHERE username = %s'
            user = username

        user = connection.get(sql, user)

        if user is not None:
            user.type = cls.USER_TYPE[user.type]

        return user
    
    @classmethod
    def query(cls):
        '''
            首页 user列表 query方法
        '''
        connection = _get_connection(cls.db)
        
        return connection.query('SELECT * FROM user WHERE type != 6')
    
    @classmethod
    def query_in_project(cls, project_id):
        '''
            获取project_id相关user
        '''
        if project_id is None:
            return None
        
        connection = _get_connection(cls.db)
        
        sql =\
            (
                'SELECT * '
                'FROM user_project '
                'NATURAL JOIN user '
                'WHERE project_id = {project_id} '
                'ORDER BY role'
            ).format(project_id=project_id)
        
        return connection.query(sql)
        

class Background(object):
    '''
        用户学历背景 background表持久化对象
    '''
    db = 'homepage'
    BACKGROUND_TYPE = TypeList(['Bachelor', 'Master', 'Ph.D'])
    
    @classmethod
    def query(cls, user_id):
        '''
            根据user_id 获取对应user背景
        '''
        #user_id 为 None
        if user_id is None:
            return None
        
        #构建数据库连接
        connection = _get_connection(cls.db)
        
        sql = (
            'SELECT * '
            'FROM user_background '
            'NATURAL JOIN background '
            'WHERE user_id = %s'
        )
        
        backgrounds = connection.query(sql, user_id)
        
        if backgrounds:
            for background in backgrounds:
                background.background_type =\
                    cls.BACKGROUND_TYPE[background.background_type]
        return backgrounds 

class Experience(object):
    '''
        工作经历 experience持久化对象
    '''
    db = 'homepage'
    
    @classmethod
    def query(cls, user_id):
        '''
            根据user_id获取对应experience
        '''
        #user_id为None
        if user_id is None:
            return None
        
        #构建数据库连接
        connection = _get_connection(cls.db)
        
        sql =\
            (
                'SELECT * '
                'FROM user_experience '
                'NATURAL JOIN experience '
                'WHERE user_id = %s'
            )
        
        return connection.query(sql, user_id)     

class Interests(object):
    '''
        研究方向 interests持久化对象
    '''
    db = 'homepage'
    
    @classmethod
    def query(cls, user_id):
        '''
            根据user_id获取对应interests
        '''
        #user_id为None
        if user_id is None:
            return None
        
        #构建数据库连接
        connection = _get_connection(cls.db)
        
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
    def get(cls, article_id):
        '''
            根据article_id获取对应文章信息
        '''
        #article_id 为None
        if article_id is None:
            return None
        
        #构建数据库连接
        connection = _get_connection(cls.db)
        
        sql =\
            (
                'SELECT * '
                'FROM article '
                'WHERE article_id = %s'
            )
        
        return connection.get(sql, article_id)
    
    @classmethod 
    def query(cls, query_num=1):
        
        query_num = query_num if query_num >= 1 else 1
        
        #构建数据库连接
        connection = _get_connection(cls.db)
        
        sql =\
            (
                'SELECT * '
                'FROM article '
                'WHERE type = 1 '
                'ORDER BY publish_time DESC '
                'LIMIT {start_num}, {end_num}'
            ).format(
                start_num=(query_num-1)*10,
                end_num=query_num*10,
            )
        
        return connection.query(sql)
    
    @classmethod
    def author(cls, author):
        #author 为None
        if author is None:
            return None
        
        author = author.strip()
        #author正常输入
        user = User.get(author)
        return user if user is not None else author
    
    @classmethod
    def authors(cls, author):
        #author 为None
        if author is None:
            return None
        
        #author正常输入
        return [ cls.author(user) for user in author.split(',') ] 
    
    @classmethod
    def chew(cls, article):
        if article is None:
            return None

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
    def get(cls, publisher_id):
        '''
            publisher get方法
        '''
        if publisher_id is None:
            return None
        
        sql =\
            (
                'SELECT * '
                'FROM publisher '
                'WHERE publisher_id = {publisher_id}'
            ).format(publisher_id=publisher_id)
        
        connection = _get_connection(cls.db)
        
        publisher = connection.get(sql)
        publisher.publisher_type = cls.PUBLISHER_TYPE[publisher.publisher_type]
        
        return publisher

class Paper(object):
    '''
        论文 Paper表持久化对象
    '''
    db = 'homepage'
    
    @classmethod
    def get(cls, article_id):
        '''
            paper get方法
        '''
        if article_id is None:
            return None
        
        sql =\
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'WHERE article_id = %s'
            )
        
        connection = _get_connection(cls.db)
        
        return connection.get(sql, article_id)
        
    @classmethod
    def query(cls, query_num=1):
        '''
            paper query方法
        '''
        
        query_num = query_num if query_num >= 1 else 1
        
        sql =\
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'NATURAL JOIN publisher '
                'WHERE article.type = 2 '
                'ORDER BY publish_year DESC '
                'LIMIT {query_start}, {query_end}'
            ).format(
                query_start=(query_num-1)*10,
                query_end=query_num*10,
            )
        
        connection = _get_connection(cls.db)

        return connection.query(sql)
    
    @classmethod
    def query_in_user(cls, user_id):
        if user_id is None:
            return None
        
        connection = _get_connection(cls.db)
        
        #构建模糊查询表达式
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
            'NATURAL JOIN publisher '
            'WHERE type = 2 '
            'AND author LIKE %s '
            'ORDER BY publish_year DESC'
        )
        
        return connection.query(sql, user_id)

    @classmethod
    def chew(cls, paper):
        if paper is None:
            return None
        
        if paper.in_press is None:
            paper.publisher = Publisher.get(paper.publisher_id)
        else:
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
    def insert(cls, **kwargs):
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
        
        connection = _get_connection(cls.db)

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
    
class PaperImage(object):
    '''
        论文图片 paperimage表持久化对象
    '''
    db = 'homepage'

    @classmethod
    def query(cls, article_id):
        '''
            获取对应article_id的images
        '''
        if article_id is None:
            return None
        
        sql =\
            (
                'SELECT * '
                'FROM paper_image '
                'WHERE article_id = %s'
            )
        
        connection = _get_connection(cls.db)
        
        return connection.query(sql, article_id)

class Item(object):
    '''
        项目类型 item表持久化对象
    '''
    db = 'homepage'
    
    @classmethod
    def query(cls, project_id):
        if project_id is None:
            return None
        
        connection = _get_connection(cls.db)
        
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
    def get(cls, project_id):
        '''
            获取对应project_id的项目信息
        '''
        if project_id is None:
            return None
        
        sql=\
            (
                'SELECT * '
                'FROM project '
                'WHERE project_id = {project_id}'
            ).format(project_id=project_id)
        
        connection = _get_connection(cls.db)
        
        return connection.get(sql)
        
    @classmethod
    def query(cls, query_num=1):
        '''
            获取10数量的project信息
        '''
        
        query_num = query_num if query_num >= 1 else 1
        
        sql =\
            (
                'SELECT * '
                'FROM project '
                'WHERE NOT ISNULL(project_null) '
                'ORDER BY start_time DESC '
                'LIMIT {start_num}, {end_num}'
            ).format(
                start_num=(query_num-1)*10,
                end_num=query_num*10,
            )
        
        connection = _get_connection(cls.db)
        
        return connection.query(sql)
    
    @classmethod
    def query_in_user(cls,user_id):
        '''
            得到与user_id相关的全部projects
        '''
        if user_id is None:
            return None
        
        connection = _get_connection(cls.db)
        
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
        if project is None:
            return None
        
        project.item = Item.query(project.project_id)

        project.users = User.query_in_project(project.project_id)
        project.project_image =\
            chewer.static_image(
                'project/'+str(project.project_id)
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
    def query_in_user(cls, user_id): 
        '''
            根据user_id得到对应奖项
        '''
        if user_id is None:
            return None
        
        connection = _get_connection(cls.db)
        
        sql =\
            (
                'SELECT * '
                'FROM user_prize '
                'NATURAL JOIN prize '
                'WHERE user_id = %s '
                'ORDER BY prize_year DESC'
            )

        return connection.query(sql, user_id)

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
    def query_in_user(cls, user_id): 
        '''
            根据user_id得到对应奖项
        '''
        if user_id is None:
            return None
        
        connection = _get_connection(cls.db)
        
        sql =\
            (
                'SELECT * '
                'FROM user_proprietary '
                'NATURAL JOIN proprietary '
                'WHERE user_id = %s '
                'ORDER BY proprietary_time DESC'
            )

        return connection.query(sql, user_id)
