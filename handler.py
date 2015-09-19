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
        self.render("index.html", page_title=u"武汉大学互联网数据挖掘实验室")

class ArticlesHandler(BaseHandler):
    '''
        文章列表页handler
    '''
    def get(self):
        self.render("articles.html", page_title=u"文章列表-武汉大学互联网数据挖掘实验室")

class ArticleHandler(BaseHandler):
    '''
        文章页handler
    '''
    def get(self):
        article = {
            "article_title" : "社交招聘的下一个技术创新方向，是推荐引擎？",
            "article_author" : u"彭敏", 
            "article_publish_time" : "2015-09-19 20:32", 
            "article_abstract" : u"开放平台时代的大数据优势，已经为社会化招聘提供了很多不同的新玩法。国外正逐渐兴起的一种新招聘模式，利用公开社交数据来挖掘合适候选人，比较典型的四家公司有Talentbin、Guild、RemarkableHire、以及Entelo.",
            "article_image" : u"switch_one.jpeg",
            "article_text" : '''<p>前几天，一位使用“今日头条”手机软件的程序员朋友，在他的头条新闻中刷出一封题为《来自“今日头条”创始人张一鸣的问候》的信。</p><p></p><p>细读之后，发现这其实是“今日头条”这家公司的一封招聘信，但形式别具一格，也颇有新意。“今日头条”本身是一款个性化的阅读软件，每个人看到的内容都不一。底层技术是基于大数据挖据的推荐引擎，自动分析每位用户的兴趣，再根据兴趣差异推荐不同的内容。这封由公司创始人张一鸣写给工程师的信正是基于推荐引擎技术，不知道收信人是谁，但如果你是工程师，并且是“今日头条”的用户，就可能在刷新“今日头条”时收到这封求贤信。</p><p></p><p>通过推荐引擎精准投放招聘广告，这是一次不错的创新，也比传统招聘中留个招聘邮箱亲和力强了太多。在此，我们暂且抛开“今日头条”这家公司不谈，一起来探讨下“数据挖据”在招聘中的潜力。</p><p></p><p>据一位非常资深的猎头说，在他经常联系的候选人名单里，20%的人有强烈的换职意向、70%的人在观望更好的工作机会，仅10%的人坚决不跳槽。</p><p></p><p>没有人会拒绝好的工作机会，但70%的观望人群不会主动更新简历，不会主动出击寻找职业机会，这个现状凸显传了统招聘模式的诸多弊端。企业与人才信息不够透明，求职者反感主动透简历的方式，尤其优秀的人才觉得这样会让自己很没面子。</p><p></p><p>而“今日头条”的这种招聘方式是一个非常好的案例，没有采用常见的通告发布，通过数据挖据让目标人才的兴趣和公司需求精确匹配，再定向个性化推送只能让该用户看到的信息，从海量数据中精确筛出目标人群，避免了简历式招聘的筛选过程，也提高了很多招聘环节的效率。当然，这种让目标人才给CEO发微博私信留电话号码的求贤方式，也让求职者得到了充分的尊重。当你接到一家高速发展期的公司创始人电话，他想约你时间喝杯咖啡时，我想这比接到人力资源部MM电话通知几点去面试要好很多。</p><p></p><p>开放平台时代的大数据优势，已经为社会化招聘提供了很多不同的新玩法。国外正逐渐兴起的一种新的招聘模式，利用公开的社交数据来挖掘合适的候选人，比较典型的四家公司有Talentbin、Guild、RemarkableHire、以及Entelo。职场社交网络LinkedIn也为中高端人才与企业招聘提供了互动平台，但还并未实现自动化的精准匹配。<strong>其收购新闻阅读应用Pulse正是出于和“今日头条”一样的尝试，试图基于数据挖掘做个性化推荐，通过推荐引擎为人才和企业双方提供精准化的对接服务。</strong></p><p></p><p>从社会化招聘到基于数据挖掘的精准招聘，推荐引擎的巨大价值由此可见一斑。当然，今日头条这家公司却志不在此，它应该努力成为手机上获取信息的入口。只是，从这家公司利用自身技术优势在招聘上的无心插柳，让我们看到了基于数据挖掘的推荐引擎在招聘领域的巨大潜力。这是一片等待开发的沃土，它为成为招聘领域发力的下一个技术创新方向吗？</p>''',
            "article_viewed" : 46,
        }
        article["article_image"] = 'img/' + article["article_image"]
        self.render(
            "article.html", 
            page_title=article["article_title"], 
            article=article,
        )

class PersonHandler(BaseHandler):
    '''
        人物页handler
    '''
    def get(self):
        person = {
            'person_realname' : 'Min Peng',
            'person_image' : 'team_head.jpeg',
        }
        person["person_image"] = 'img/' + person["person_image"]
        self.render(
            "person.html", 
            page_title=\
                person['person_realname'] \
                    +u"武汉大学互联网数据挖掘实验室",
            person=person,
        )
