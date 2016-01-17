# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月23日 星期三 13时50分22秒
#
'''
    数据层测试文件
'''

from nose.tools import assert_equal
import database
import mock
import logging
import copy
import datetime


@mock.patch('logging.error')
@mock.patch('torndb.Connection')
@mock.patch('config.Config')
def test_get_connection(mock_config, mock_connection, mock_error):
    class test_c(object):

        @classmethod
        @database.get_connection
        def test_connection(cls, connection):
            return 'test'

        @classmethod
        @database.get_connection
        def test_query(cls, connection):
            return ['test']

    mock_config.MYSQL_ADDRESS = 'test'
    mock_config.MYSQL_PORT = 'test'
    mock_config.MYSQL_USER = 'test'
    mock_config.MYSQL_PASSWD = 'test'

    result = test_c.test_connection()
    assert result is None
    mock_error.assert_called_with(
        'Mysql Connection Error: class test_c db not assigned')

    result = test_c.test_query()
    assert_equal(result, [])

    test_c.db = 'test'
    result = test_c.test_connection()
    assert_equal(result, 'test')
    mock_connection.assert_called_with(
        'test:test',
        'test',
        'test',
        'test',
    )

    test_c.db = 'test'
    result = test_c.test_query()
    assert_equal(result, ['test'])


@mock.patch.object(logging, "error")
def test_typelist_getitem(mock_logging_error):
    example = database.TypeList([1])
    # 越界异常
    test_result = example[2]
    assert mock_logging_error.called
    assert_equal(test_result, 'Unknown')

    # 正常输入
    assert_equal(example[1], 1)


def test_typelist_index():
    example = database.TypeList([1])

    # 正常输入
    assert_equal(example.index(1), 1)


class TestPersistence(object):
    '''
        持久化对象测试类
    '''

    def setUp(self):
        '''
            持久化对象测试初始化
        '''
        # 捕获数据库连接并用mock模拟
        self.mock_db = mock.Mock()
        patch = mock.patch('torndb.Connection')
        self.mock_connection = patch.start()
        self.mock_connection.return_value = self.mock_db

    def test_user_get_user_id(self):
        # mock构建
        mock_user = mock.Mock()
        self.mock_db.get.return_value = mock_user

        # user_id输入
        assert_equal(database.User.get_in_user_id(1), mock_user)
        self.mock_db.get.assert_called_with(
            'SELECT * FROM user WHERE user_id = %s', 1)

    def test_user_get_username(self):
        # mock构建
        mock_user = mock.Mock()
        self.mock_db.get.return_value = mock_user

        # user_id输入
        assert_equal(database.User.get_in_username(1), mock_user)
        self.mock_db.get.assert_called_with(
            'SELECT * FROM user WHERE username = %s', 1)

    def test_user_query(self):
        # mock构建
        mock_user = mock.Mock()
        self.mock_db.query.return_value = [mock_user]

        # 正常输入
        # request_type未输入
        users = database.User.query()
        self.mock_db.query.assert_called_with((
            'SELECT * '
            'FROM user '
            'WHERE type != {visitor_type} '
            'ORDER BY type'
        ).format(visitor_type=database.User.USER_TYPE.index('Visitor')))
        assert_equal(users, [mock_user])

        # request_type输入
        users = database.User.query(1)
        self.mock_db.query.assert_called_with((
            'SELECT * '
            'FROM user '
            'WHERE type = 1'
        ))
        assert_equal(users, [mock_user])

    def test_user_query_in_project(self):
        # mock构建
        mock_user = mock.Mock()
        self.mock_db.query.return_value = [mock_user]

        users = database.User.query_in_project(1)
        self.mock_db.query.assert_called_with(
            'SELECT * '
            'FROM user_project '
            'NATURAL JOIN user '
            'WHERE project_id = 1 '
            'ORDER BY role'
        )
        assert_equal(users, [mock_user])

    def test_user_chew(self):
        # mock构建
        mock_user = mock.Mock()
        mock_user.user_id = '1'
        mock_user.firstname = 'test'
        mock_user.lastname = 'test'
        mock_user.type = 1

        user = database.User.chew(mock_user)
        assert_equal(user.image, 'img/person/1.jpeg')
        assert_equal(user.english_name, 'Test Test')
        assert_equal(user.type, database.User.USER_TYPE[1])

    def test_background_query(self):
        # mock构建
        mock_background = mock.Mock()
        self.mock_db.query.return_value = [mock_background]

        backgrounds = database.Background.query(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM user_background '
                'NATURAL JOIN background '
                'WHERE user_id = %s '
                'ORDER BY background_type'
            ),
            1
        )
        assert_equal(backgrounds, [mock_background])

    def test_background_chew(self):
        # mock构建
        mock_background = mock.Mock()
        mock_background.background_type = 1
        mock_background.start_time = datetime.date(2015, 01, 01)
        mock_background.end_time = datetime.date(2015, 01, 01)

        background = database.Background.chew(mock_background)
        assert_equal(background.background_type,
                     database.Background.BACKGROUND_TYPE[1])
        assert_equal(background.start_time, '01/2015')
        assert_equal(background.end_time, '01/2015')

    def test_experience_query(self):
        # mock构建
        mock_experience = mock.Mock()
        self.mock_db.query.return_value = [mock_experience]

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

    def test_experience_chew(self):
        # mock构建
        mock_experience = mock.Mock()
        mock_experience.start_time = datetime.date(2015, 01, 01)
        mock_experience.end_time = datetime.date(2015, 01, 01)

        experience = database.Experience.chew(mock_experience)

        assert_equal(experience.start_time, '01/2015')
        assert_equal(experience.end_time, '01/2015')

    def test_interests_query(self):
        # mock构建
        mock_interests = mock.Mock()
        self.mock_db.query.return_value = [mock_interests]

        # user_id正常输入
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
        # mock构建
        mock_article = mock.Mock()
        self.mock_db.get.return_value = mock_article

        # 正常输入
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
        # mock 构建
        mock_article = mock.Mock()
        self.mock_db.query.return_value = [mock_article]

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
        with mock.patch("database.User.get_in_user_id"):
            # author为内置user
            with mock.patch("database.User.chew"):
                database.User.get_in_user_id.return_value = 2
                database.User.chew.return_value = 2
                author = database.Article.author('test')
                assert_equal(author, 2)
                database.User.chew.assert_called_with(2)
            # author非内置user
            database.User.get_in_user_id.return_value = None
            author = database.Article.author('test')
            assert_equal(author, 'test')

    def test_article_authors(self):
        # 构建mock
        mock_author = mock.Mock()

        with mock.patch("database.Article.author"):
            database.Article.author.return_value = mock_author
            assert_equal(database.Article.authors('1'), [mock_author])
            database.Article.author.assert_called_with('1')

    def test_article_chew(self):
        # 构建mock
        mock_article = mock.Mock()
        mock_article.article_id = 1
        mock_article.abstract = 'test'
        mock_article.author = 'test'

        # 正常处理
        with mock.patch('database.Article.authors'):
            article = database.Article.chew(mock_article)
            assert_equal(article.article_image, 'img/1.jpeg')
            assert_equal(article.short_abstract, 'test')
            database.Article.authors.assert_called_with('test')

    def test_publisher_get(self):
        # 构建mock
        mock_publisher = mock.Mock()
        self.mock_db.get.return_value = mock_publisher

        publisher = database.Publisher.get(1)
        self.mock_db.get.assert_called_with(
            (
                'SELECT * '
                'FROM publisher '
                'WHERE publisher_id = 1'
            ),
        )
        assert_equal(publisher, mock_publisher)

    def test_publisher_chew(self):
        # 构建mock
        mock_publisher = mock.Mock()
        mock_publisher.publisher_type = 1

        publisher = database.Publisher.chew(mock_publisher)
        assert_equal(publisher.publisher_type,
                     database.Publisher.PUBLISHER_TYPE[1])

    def test_paper_get(self):
        # 构建mock
        mock_paper = mock.Mock()
        self.mock_db.get.return_value = mock_paper

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
        # 构建mock
        mock_paper = mock.Mock()
        self.mock_db.query.return_value = [mock_paper]

        papers = database.Paper.query()
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'WHERE article.type = 2 '
                'ORDER BY publish_year DESC '
                'LIMIT 0, 10'
            )
        )
        assert_equal(papers, [mock_paper])

    def test_paper_query_in_year(self):
        # 构造mock
        mock_project = mock.Mock()
        self.mock_db.query.return_value = [mock_project]

        projects = database.Paper.query_in_year('2015')
        self.mock_db.query.assert_called_with((
            'SELECT * '
            'FROM article '
            'NATURAL JOIN paper '
            'WHERE publish_year = %s'
        ), '2015-01-01')
        assert_equal(projects, [mock_project])

    def test_paper_query_in_user(self):
        # 构建mock
        mock_paper = mock.Mock()
        self.mock_db.query.return_value = [mock_paper]

        papers = database.Paper.query_in_user(1)
        self.mock_db.query.assert_called_with(
            (
                'SELECT * '
                'FROM article '
                'NATURAL JOIN paper '
                'WHERE type = 2 '
                'AND author LIKE %s '
                'ORDER BY publish_year DESC'
            ),
            '%1%',
        )
        assert_equal(papers, [mock_paper])

    def test_paper_insert(self):
        # 构造输入
        insert = {
            'title': 'test',
            'author': 'test',
            'abstract': 'test',
            'publisher_id': 1,
            'start_page': 1,
            'end_page': 1,
            'volume': 1,
            'number': 1,
            'publish_year': '2010-01-01',
            'paper_url': 'http',
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

        # 异常输入
        for value in request_value:
            # 需求值未给出
            mock_insert = copy.deepcopy(insert)
            mock_insert.pop(value)
            assert_equal(database.Paper.insert(**mock_insert), False)
            # 需求值为None
            mock_insert = copy.deepcopy(insert)
            mock_insert[value] = None
            assert_equal(database.Paper.insert(**mock_insert), False)

        # 正常输入
        assert_equal(database.Paper.insert(**insert), True)

        # 异常捕获
        self.mock_db.execute.side_effect = Exception('test')
        with mock.patch('logging.error'):
            assert_equal(database.Paper.insert(**insert), False)
            logging.error.assert_called_with(
                'paper insert error in article: test')

    def test_paper_chew(self):
        # 构造mock
        mock_paper = mock.Mock()
        mock_paper.publish_year = datetime.date(2015, 01, 01)
        mock_paper.author = 'test'
        mock_paper.abstract = 'test'
        mock_paper.publisher_id = 1
        mock_paper.title = 'test'
        mock_paper.article_id = 'test'

        # 校验处理
        with mock.patch('database.Article.authors'),\
                mock.patch('database.Publisher.get'),\
                mock.patch('database.Publisher.chew'):
            # paper in press
            mock_paper.in_press = 'test'
            # paper pdf url
            mock_paper.paper_url = None
            database.Paper.chew(mock_paper)
            assert_equal(mock_paper.title, 'test(In Press)')
            assert_equal(mock_paper.pdf_url, 'paper/test.pdf')
            assert_equal(mock_paper.short_abstract, 'test')
            assert_equal(mock_paper.publish_year, '2015')
            database.Article.authors.assert_called_with('test')

            # paper not in press
            mock_paper.in_press = None
            database.Paper.chew(mock_paper)
            database.Publisher.get.assert_called_with(1)

    def test_item_query(self):
        # 构造mock
        mock_item = mock.Mock()
        self.mock_db.query.return_value = [mock_item]

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
        # 构造mock
        mock_project = mock.Mock()
        self.mock_db.get.return_value = mock_project

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
        # 构造mock
        mock_project = mock.Mock()
        self.mock_db.query.return_value = [mock_project]

        projects = database.Project.query()
        self.mock_db.query.assert_called_with((
            'SELECT * '
            'FROM project '
            'ORDER BY start_time DESC '
            'LIMIT 0, 10'
        ))
        assert_equal(projects, [mock_project])

    def test_project_query_in_year(self):
        # 构造mock
        mock_project = mock.Mock()
        self.mock_db.query.return_value = [mock_project]

        projects = database.Project.query_in_year('2015')
        self.mock_db.query.assert_called_with((
            'SELECT * '
            'FROM project '
            'WHERE end_time >= %s '
            'ORDER BY start_time DESC '
        ), '2015-01-01')
        assert_equal(projects, [mock_project])

    def test_project_query_in_user(self):
        # 构建mock
        mock_project = mock.Mock()
        self.mock_db.query.return_value = [mock_project]

        database.Project.query_in_user(1)
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
        # 构造mock
        mock_project = mock.Mock()
        mock_project.project_id = 1
        mock_project.start_time = datetime.date(2015, 01, 01)
        mock_project.end_time = datetime.date(2015, 01, 01)

        with mock.patch('database.Item.query'),\
                mock.patch('database.User.query_in_project'),\
                mock.patch('database.User.chew'):
            database.User.query_in_project.return_value = [1]
            database.Project.chew(mock_project)
            database.Item.query.assert_called_with(1)
            database.User.query_in_project.assert_called_with(1)
            database.User.chew.assert_called_with(1)
            assert_equal(mock_project.project_image, 'img/project/1.jpeg')
            assert_equal(mock_project.start_time, '01/2015')
            assert_equal(mock_project.end_time, '01/2015')

    def test_prize_query_in_user(self):
        # 构建mock
        mock_prize = mock.Mock()
        self.mock_db.query.return_value = [mock_prize]

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

    def test_prize_chew(self):
        # 构建mock
        mock_prize = mock.Mock()
        mock_prize.prize_year = datetime.date(2015, 01, 01)
        mock_prize.prize_facility = None

        prize = database.Prize.chew(mock_prize)
        assert_equal(prize.prize_year, '2015')
        assert_equal(prize.prize_facility, '')

    def test_proprietary_query_in_user(self):
        # 构建mock
        mock_proprietary = mock.Mock()
        self.mock_db.query.return_value = [mock_proprietary]

        # 正常输入
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

    def test_proprietary_chew(self):
        # 构建mock
        mock_proprietary = mock.Mock()
        mock_proprietary.proprietary_time = datetime.date(2015, 01, 01)

        proprietary = database.Proprietary.chew(mock_proprietary)
        assert_equal(proprietary.proprietary_time, '2015')
