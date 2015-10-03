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

class PersonIndicatorModule(tornado.web.UIModule):
    '''
        用户页右侧悬浮
    '''
    def render(self):
        return \
        '''
            <div id="PersonIndicator">
                <div><a href="#BasicInfo">Basic</a></div>
                <div><a href="#PersonalInfo">Personal</a></div>
                <div><a href="#BIO">BIO</a></div>
                <div><a href="#EducationBackground">Education</a></div>
                <div><a href="#WorkExperience">Experience</a></div>
                <div><a href="#ScientificResearch">Research</a></div>
                <div><a href="#MainPublishedPapers">Papers</a></div>
                <div><a href="#MainItemsandResearch">Items</a></div>
                <div><a href="#ResearchPrize">Prize</a></div>
                <div><a href="#Others">Others</a></div>
            </div>
        '''
    
    def embedded_css(self):
        return \
        '''
            #PersonIndicator{
                position: fixed;
                bottom: 25px;
                right: 15%;
            }
            #PersonIndicator a, a:hover, a:focus{
                text-decoration: none;
                color: #333;
            }
        '''
    
    
   
