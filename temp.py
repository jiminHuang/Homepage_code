# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月29日 星期二 20时11分02秒
#
import database
import hashlib

insert = {
    'title' : 'Wireless Service Attributes Classification and Matching Mechanism Based on Decision Tree',
    'author' : '60da69f18080728b870d3c75ffb74a105ff10022,Laurence T. Yang, W. Zhao, N. Xiong',
    'abstract' : 'In this paper, SeviceCuts, a decision tree based model is proposed, considering the special attributes of wireless service and the normal need of users, helping service decision agent classify the wireless services adaptively. The decision tree is traversed based on some searching rule. A small number of matching rules are stored in the leaf node, which contain the most matching service strategies to users, and are linearly traversed to find the highest priority rule that matches the user\'s query requirement. The analysis of algorithm complication and performance shows that the efficiency of ServiceCuts decision tree model is better than traditional linear search structure and the normal binary decision tree structure.',
    'publisher_id' : 19,
    'start_page' : 12,
    'end_page' : 17,
    'publish_year' : '2008-01-01',
    #'paper_url' : 'http://www.scholarmate.com/scmwebsns/publication/view;jsessionid=EDDC4CBA538285AE1B3F0AFB57C92121-n1.snsweb2001?des3Id=X%252BI6qKUj%252B6lQ49s2n%252Fk95w%253D%253D',
}

if database.Paper.insert(**insert):
    print 'success'
else:
    print 'failed'

print hashlib.md5(insert['title']).hexdigest()
