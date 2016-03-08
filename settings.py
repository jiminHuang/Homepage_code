# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月03日 星期四 14时26分03秒
#
import modules
import config

settings = {
    'debug': True,  # 调试选项，开启后每一次源文件的更改将会自动重启服务器(而不需要手动操作)
    'autoescape': None,  # 新添加，不知会妨碍原程序与否
    'login_url': '/login',
    'cookie_secret': config.Config.COOKIE_SECRET,
    'static_path': config.Config.get_local_position('static'),
    'template_path': config.Config.get_local_position('template'),
    'ui_modules': {
        'List': modules.ListModule,
        'SinglePage': modules.SinglePageModule,
        'ResearchItem': modules.ResearchListItemModule,
        'ArticleItem': modules.ArticleListItemModule,
        'ProjectItem': modules.ProjectListItemModule,
        'TeamSelector': modules.TeamSelectorModule,
        'TeamMember': modules.TeamMemberModule,
        'ModelItem': modules.ModelListItemModule,
    }
    # 'log_file_prefix': '8888.log',
}
