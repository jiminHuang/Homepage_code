# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月16日 星期三 20时36分43秒
#
'''
    包含前端模块定义的文件
'''
import tornado.web

class ListModule(tornado.web.UIModule):
    '''
        列表页公用css
    '''
    def render(self):
        return ''
    
    def css_files(self):
        return "/static/css/list.css"
    
    def javascript_files(self):
        return "/static/js/list.js"

class SinglePageModule(tornado.web.UIModule):
    '''
        内容单页公用css
    '''
    def render(self):
        return ''
    
    def css_files(self):
        return "/static/css/single.css"

class ResearchListItemModule(tornado.web.UIModule):
    '''
        Research页列表项模块
    '''
    def render(self, paper):
        return self.render_string('module/researchItem.html', paper=paper)

class ArticleListItemModule(tornado.web.UIModule):
    '''
        文章列表页列表项模块
    '''
    def render(self, article):
        return self.render_string('module/articleItem.html', article=article)

class ProjectListItemModule(tornado.web.UIModule):
    '''
        项目列表页列表项模块
    '''
    def render(self, project):
        return self.render_string('module/projectItem.html', project=project)

class TeamSelectorModule(tornado.web.UIModule):
    '''
        首页team选择模块
    '''
    def render(self):
        return ''
    
    def javascript_files(self):
        return "/static/js/team_selector.js"

class TeamMemberModule(tornado.web.UIModule):
    '''
        首页team 人员项模块
    '''
    def render(self, person):
        return self.render_string('module/teamMember.html', person=person)
