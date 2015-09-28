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

def _get_connection(db):
    '''
        获取数据库连接函数
    '''
    return torndb.Connection(
        ":".join(
            [config.get_database_address(),
            config.get_database_port()]
        ),
        db,
        config.get_database_user(),
        config.get_database_password(),
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
        
        article = connection.get(sql, article_id)
        
        if article is not None:
            article.author =\
                [
                    User.get(user_id = author)
                        if User.get(user_id = author) else author
                            for author in article.author.split(',')
                ]
        return article
    
    @classmethod 
    def query(cls, article_id=None):
        #构建数据库连接
        connection = _get_connection(cls.db)
        
        sql =\
            (
                'SELECT * '
                'FROM article'
            )
        
        article = cls.get(article_id)
        
        sql =\
            ' '.join((
                sql,
                'WHERE publish_time > UNIX_TIMESTAMP(%s)'\
                    if article is not None else '',
                'ORDER BY publish_time',
                'LIMIT 10',
            ))
        
        if article is not None:
            articles = connection.query(sql, article.publish_time)
        else:
            articles = connection.query(sql)
        
        for article in articles:
            article.author =\
                [
                    User.get(user_id = author)
                        if User.get(user_id = author) else None 
                            for author in article.author.split(',')
                ]
        
        return articles
    
class Publisher(object):
    '''
        出版 Publisher表持久化对象
    '''
    db = 'homepage'
    PUBLISHER_TYPE = TypeList(['Meeting', 'Journal'])
    
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
        publisher.type = cls.PUBLISHER_TYPE[publisher.type]
        
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
        
        paper = Article.get(article_id)
        if paper is None:
            return None

        sql =\
            (
                'SELECT * '
                'FROM paper '
                'WHERE article_id = %s'
            )
        
        connection = _get_connection(cls.db)
        
        paper_info = connection.get(sql, article_id)
        
        if paper_info is None:
            return None
        
        paper.update(paper_info)
        
        paper.publisher = Publisher.get(paper_info.publisher_id)
        return paper
