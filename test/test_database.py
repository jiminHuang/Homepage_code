# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月23日 星期三 13时50分22秒
#
'''
    数据层测试文件
'''

from nose.tools import *
import database
import torndb
import mock
import logging
import copy
import chewer

@mock.patch.object(logging, "error")
def test_typelist_getitem(mock_logging_error):
    example = database.TypeList([1])
    
    #越界异常
    test_result = example[2]
    assert mock_logging_error.called 
    assert_equal(test_result, 'Unknown')
    
    #正常输入
    assert_equal(example[1], 1)


class TestPersistence(object):
    '''
        持久化对象测试类
    '''

    def setUp(self):
        '''
            持久化对象测试初始化
        '''
        #捕获数据库连接并用mock模拟
        self.mock_db = mock.Mock()
        patch = mock.patch('database._get_connection')
        self.mock_connection = patch.start()
        self.mock_connection.return_value = self.mock_db

    def test_user_get(self):
        #user_id未输入
        user = database.User.get()
        assert user is None
        
        #mock构建
        mock_user = mock.Mock()
        mock_user.type = 1
        self.mock_db.get.return_value = mock_user
        
        #user_id输入
        user = database.User.get(user_id=1)
        self.mock_db.get.assert_called_with('SELECT * FROM user WHERE user_id = %s', 1)
        
        #username输入
        mock_user.type = 1
        user = database.User.get(username=1)
        self.mock_db.get.assert_called_with('SELECT * FROM user WHERE username = %s', 1)
        
        #user不存在
        self.mock_db.get.return_value = None
        user = database.User.get(username=1)
        assert user is None
    
    def test_user_query(self):
        #mock构建
        mock_user = mock.Mock()
        self.mock_db.query.return_value = [mock_user]
        
        #正常输入
        users = database.User.query()
        self.mock_db.query.assert_called_with('SELECT * FROM user WHERE type != 6')
        assert_equal(users, [mock_user])
    
    def test_user_query_in_project(self):
        #project_id未输入
        assert_raises(TypeError, database.User.query_in_project)
        
        #project_id输入为None
        assert database.User.query_in_project(None) is None
        
        #mock构建
        mock_user = mock.Mock()
        self.mock_db.query.return_value = [mock_user]
        
        #正常输入
        users = database.User.query_in_project(1)
        self.mock_db.query.assert_called_with(
            'SELECT * '
            'FROM user_project '
            'NATURAL JOIN user '
            'WHERE project_id = 1 '
            'ORDER BY role'
        )
        assert_equal(users, [mock_user])
        
    def test_background_query(self):
        #user_id未输入
        assert_raises(TypeError, database.Background.query)

        #user_id输入为空
        user = database.Background.query(None)
        assert user is None
        
        #mock构建
        mock_background = mock.Mock()
        mock_background.background_type = 1
        self.mock_db.query.return_value = [mock_background]
    
        #user_id正常输入
        backgrounds = database.Background.query(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_background '
                'NATURAL JOIN background '
                'WHERE user_id = %s'
            ),
            1
        )
        assert_equal(backgrounds, [mock_background])
        
        #backgrounds无
        self.mock_db.query.return_value = []
        backgrounds = database.Background.query(1)
        assert_equal(backgrounds, [])
        
    def test_experience_query(self):
        #user_id未输入
        assert_raises(TypeError, database.Experience.query)

        #user_id输入为空
        user = database.Experience.query(None)
        assert user is None
        
        #mock构建
        mock_experience = mock.Mock()
        self.mock_db.query.return_value = [mock_experience]
        
        #user_id正常输入
        experiences = database.Experience.query(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_experience '
                'NATURAL JOIN experience '
                'WHERE user_id = %s'
            ),
            1
        )
        assert_equal(experiences, [mock_experience])
    
    def test_interests_query(self):
        #user_id未输入
        assert_raises(TypeError, database.Interests.query)

        #user_id输入为空
        user = database.Interests.query(None)
        assert user is None
        
        #mock构建
        mock_interests = mock.Mock()
        self.mock_db.query.return_value = [mock_interests]
        
        #user_id正常输入
        interests = database.Interests.query(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_interests '
                'NATURAL JOIN interests '
                'WHERE user_id = %s'
            ),
            1
        )
        assert_equal(interests, [mock_interests])
        
    def test_article_get(self):
        #article_id未输入
        assert_raises(TypeError, database.Article.get)
        
        #article_id输入为空
        article = database.Article.get(None) 
        assert article is None
        
        #mock构建
        mock_article = mock.Mock()
        mock_article.author = "1"
        self.mock_db.get.return_value = mock_article
        
        #正常输入
        article = database.Article.get(1)
        self.mock_db.get.assert_called_with(
            (
                'SELECT * '
                'FROM article '
                'WHERE article_id = %s'
            ),
            1
        )
        assert_equal(article, mock_article)
    
    def test_articles_query(self):
        #mock 构建
        mock_article = mock.Mock()
        self.mock_db.query.return_value = [mock_article]
        
        #正常输入
        articles = database.Article.query()

        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM article '
                'WHERE type = 1 '
                'ORDER BY publish_time DESC '
                'LIMIT 0, 10'
            )
        )
        assert_equal(articles, [mock_article])

    def test_article_author(self):
        #author未输入
        assert_raises(TypeError, database.Article.author)
        
        #author为None或空
        assert database.Article.author(None) is None
    
        #author正常输入
        with mock.patch("database.User.get"):
            #author为内置user
            database.User.get.return_value = 2
            author = database.Article.author('test')
            assert_equal(author, 2)
            #author非内置user
            database.User.get.return_value = None
            author = database.Article.author('test')
            assert_equal(author, 'test')
    
    def test_article_authors(self):
        #author未输入
        assert_raises(TypeError, database.Article.authors)
        
        #author为None或空
        assert database.Article.authors(None) is None
        
        #构建mock
        mock_author = mock.Mock()

        #author正常输入
        with mock.patch("database.Article.author"):
            database.Article.author.return_value = mock_author
            assert_equal(database.Article.authors('1'), [mock_author])
            database.Article.author.assert_called_with('1')
       
    def test_article_chew(self):
        #author未输入
        assert_raises(TypeError, database.Article.authors)
        
        #author为None或空
        assert database.Article.authors(None) is None
        
        #构建mock
        mock_article = mock.Mock()
        mock_article.article_id = 1
        mock_article.abstract = 'test'
        mock_article.author = 'test'
    
        #正常处理
        with mock.patch('database.Article.authors'):
            article = database.Article.chew(mock_article)
            assert_equal(article.article_image, 'img/1.jpeg')
            assert_equal(article.short_abstract, 'test')
            database.Article.authors.assert_called_with('test')
             
    def test_publisher_get(self):
        #publisher_id 
        assert_raises(TypeError, database.Publisher.get)
        
        #publisher_id输入为空
        publisher = database.Publisher.get(None) 
        assert publisher is None
        
        #构建mock
        mock_publisher = mock.Mock()
        mock_publisher.publisher_type = 1
        self.mock_db.get.return_value = mock_publisher
        
        #正常输入
        publisher = database.Publisher.get(1)
        self.mock_db.get.assert_called_with(
            (
                'SELECT * '
                'FROM publisher '
                'WHERE publisher_id = 1'
            ),
        )
        assert_equal(publisher, mock_publisher)
        assert_equal(publisher.publisher_type, database.Publisher.PUBLISHER_TYPE[1]) 
        
    def test_paper_get(self):
        #article_id未输入
        assert_raises(TypeError, database.Paper.get)
        
        #article_id输入为空
        paper = database.Paper.get(None) 
        assert paper is None
        
        #构建mock
        mock_paper = mock.Mock()
        self.mock_db.get.return_value = mock_paper
        
        #正常输入
        paper = database.Paper.get(1)
        self.mock_db.get.assert_called_with(
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'WHERE article_id = %s'
            ),
            1,
        )
        assert_equal(paper, mock_paper)
    
    def test_paper_query(self):
        #构建mock
        mock_paper = mock.Mock()
        mock_paper.publish_year = 1
        mock_paper.article_id = 1
        self.mock_db.query.return_value = [mock_paper]
        
        #正常输入
        #article_id未输入
        papers = database.Paper.query() 
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'NATURAL JOIN publisher '
                'WHERE article.type = 2 '
                'ORDER BY publish_year DESC '
                'LIMIT 0, 10'
            )
        )
        assert_equal(papers, [mock_paper])
        #article_id已输入
        #提供的article_id 可以得到对应paper
        papers = database.Paper.query(2)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'NATURAL JOIN publisher '
                'WHERE article.type = 2 '
                'ORDER BY publish_year DESC '
                'LIMIT 10, 20'
            ),
        )
          
    def test_paper_query_in_user(self):
        #user_id未输入
        assert_raises(TypeError, database.Paper.query_in_user)
        
        #user_id输入为None
        assert database.Paper.query_in_user(None) is None
        
        #构建mock
        mock_paper = mock.Mock()
        self.mock_db.query.return_value = [mock_paper]
        
        #正常输入
        papers = database.Paper.query_in_user(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'NATURAL JOIN publisher '
                'WHERE type = 2 '
                'AND author LIKE %s '
                'ORDER BY publish_year DESC'
            ),
            '%1%',
        )
        assert_equal(papers, [mock_paper])
    
    def test_paper_insert(self):
        #构造输入
        insert = {
            'title' : 'test',
            'author' : 'test',
            'abstract' : 'test',
            'publisher_id' : 1,
            'start_page' : 1,
            'end_page' : 1,
            'volume' : 1,
            'number' : 1,
            'publish_year' : '2010-01-01',
            'paper_url' : 'http',
        }
        request_value = [
            'title', 
            'author', 
            'abstract', 
            'publisher_id', 
            'start_page',
            'end_page',
            'publish_year',
        ]
        
        #异常输入
        for value in request_value:
            #需求值未给出
            mock_insert = copy.deepcopy(insert)
            mock_insert.pop(value)
            assert_equal(database.Paper.insert(**mock_insert), False)
            #需求值为None
            mock_insert = copy.deepcopy(insert)
            mock_insert[value] = None
            assert_equal(database.Paper.insert(**mock_insert), False)
    
        #正常输入
        assert_equal(database.Paper.insert(**insert), True)
        
        #异常捕获
        self.mock_db.execute.side_effect = Exception('test')
        with mock.patch('logging.error'):
            assert_equal(database.Paper.insert(**insert), False)
            logging.error.assert_called_with('paper insert error in article: test')
    
    def test_paper_chew(self):
        #paper未输入
        assert_raises(TypeError, database.Paper.chew)
        
        #paper为None
        assert database.Paper.chew(None) is None
        
        #构造mock
        mock_paper = mock.Mock()
        mock_paper.publish_year = '2015-01-01'
        mock_paper.author = 'test'
        mock_paper.abstract = 'test'
        mock_paper.publisher_id = 1
        mock_paper.title = 'test'
        mock_paper.article_id = 'test'
        
        #校验处理
        with mock.patch('chewer.strftime_present'),\
            mock.patch('database.Article.authors'),\
            mock.patch('chewer.text_cutter'),\
            mock.patch('database.Publisher.get'):
            #paper in press
            mock_paper.in_press = 'test'
            #paper pdf url
            mock_paper.paper_url = None
            paper = database.Paper.chew(mock_paper)
            assert_equal(mock_paper.title, 'test(In Press)')
            assert_equal(mock_paper.pdf_url, 'paper/test.pdf')
            chewer.text_cutter.assert_called_with('test', 255)
            database.Article.authors.assert_called_with('test')
            chewer.strftime_present.assert_called_with('%Y', '2015-01-01')
            
            #paper not in press
            mock_paper.in_press = None
            paper = database.Paper.chew(mock_paper)
            database.Publisher.get.assert_called_with(1)

    def test_paper_image_query(self):
        #article_id未输入
        assert_raises(TypeError, database.PaperImage.query)
        
        #article_id为None
        assert database.PaperImage.query(None) is None
        
        #构造mock
        mock_image = mock.Mock()
        self.mock_db.query.return_value = mock_image
        
        #正常输入
        image = database.PaperImage.query(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM paper_image '
                'WHERE article_id = %s'
            ),
            1
        )
        assert_equal(image, mock_image)
    
    def test_item_query(self):
        #project_id未输入
        assert_raises(TypeError, database.Project.get)
        
        #project_id为None
        assert database.Project.get(None) is None
        
        #构造mock
        mock_item= mock.Mock()
        self.mock_db.query.return_value = [mock_item]
        
        #正常输入
        items = database.Item.query(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM project_item '
                'NATURAL JOIN item '
                'WHERE project_id = 1'
            )
        )
        assert_equal(items, [mock_item])

    def test_project_get(self):
        #project_id未输入
        assert_raises(TypeError, database.Project.get)
        
        #project_id为None
        assert database.Project.get(None) is None
        
        #构造mock
        mock_project = mock.Mock() 
        self.mock_db.get.return_value = mock_project
        
        #正常输入
        project = database.Project.get(1)
        self.mock_db.get.assert_called_with(
            (
                'SELECT * '
                'FROM project '
                'WHERE project_id = 1'
            ),
        )
        assert_equal(project, mock_project)

    def test_project_query(self):
        #构造mock
        mock_project = mock.Mock()
        self.mock_db.query.return_value = [mock_project]
        
        projects = database.Project.query()
        self.mock_db.query.assert_called_with((
            'SELECT * '
            'FROM project '
            'WHERE NOT ISNULL(project_null) '
            'ORDER BY start_time DESC '
            'LIMIT 0, 10'
        ))
    
    def test_project_query_in_user(self):
        #user_id未输入
        assert_raises(TypeError, database.Project.query_in_user)
        
        #user_id为None
        assert database.Project.query_in_user(None) is None
        
        #构建mock
        mock_project = mock.Mock()
        self.mock_db.query.return_value = [mock_project]        

        #user_id正常输入
        projects = database.Project.query_in_user(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_project '
                'NATURAL JOIN project '
                'WHERE user_id = %s '
                'ORDER BY start_time DESC'
            ),
            1
        )
    
    def test_project_chew(self):
        #project未输入
        assert_raises(TypeError, database.Project.chew)
        
        #project为None
        assert database.Project.chew(None) is None
        
        #构造mock
        mock_project = mock.Mock() 
        mock_project.project_id = 1
        mock_project.start_time = '2015-01-01'
        mock_project.end_time = '2015-01-01'
        
        with mock.patch('database.Item.query'),\
            mock.patch('database.User.query_in_project'),\
            mock.patch('chewer.strftime_present'):
            project = database.Project.chew(mock_project)
            database.Item.query.assert_called_with(1)
            database.User.query_in_project.assert_called_with(1)
            chewer.strftime_present.assert_called_with('%m/%Y', '2015-01-01')
            assert_equal(mock_project.project_image, 'img/project/1.jpeg')
    
    def test_prize_query_in_user(self):
        #user_id未输入
        assert_raises(TypeError, database.Prize.query_in_user)
        
        #user_id为None
        assert database.Prize.query_in_user(None) is None
        
        #构建mock
        mock_prize = mock.Mock()
        self.mock_db.query.return_value = [mock_prize]        
        
        #正常输入
        prizes = database.Prize.query_in_user(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_prize '
                'NATURAL JOIN prize '
                'WHERE user_id = %s '
                'ORDER BY prize_year DESC'
            ),
            1
        )
        assert_equal(prizes, [mock_prize])
    
    def test_proprietary_query_in_user(self):
        #user_id未输入
        assert_raises(TypeError, database.Proprietary.query_in_user)
        
        #user_id为None
        assert database.Proprietary.query_in_user(None) is None
        
        #构建mock
        mock_proprietary = mock.Mock()
        self.mock_db.query.return_value = [mock_proprietary]        
        
        #正常输入
        proprietaries = database.Proprietary.query_in_user(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_proprietary '
                'NATURAL JOIN proprietary '
                'WHERE user_id = %s '
                'ORDER BY proprietary_time DESC'
            ),
            1
        )
        assert_equal(proprietaries, [mock_proprietary])
