# coding=utf-8
import json

import requests

lines = """http://vote.weibo.com/poll/138038117
http://vote.weibo.com/poll/138038048
http://vote.weibo.com/poll/138170682
http://vote.weibo.com/poll/138230476
http://vote.weibo.com/poll/138233772
http://vote.weibo.com/poll/138251803
http://vote.weibo.com/poll/138258645
http://vote.weibo.com/poll/138258636
http://vote.weibo.com/poll/138258647"""

lines = lines.split('\n')
from pyquery import PyQuery as pq

ans = {}

for line in lines:
    line = line.strip()
    req = requests.get(line)
    doc = pq(req.text)
    flag = doc('.sele_but >a').text()
    title = doc('.W_f18').text()
    lists = doc('.text_li')
    lists1 = doc('.img_li')
    lists.extend(lists1)
    # print flag
    if flag == u'已结束':
        pass
    else:
        option = -1
        for li in pq(lists):
            if u'大张伟' in pq(li).text():
                option = pq(li).attr('data')
                print pq(li).text(), option
        print title, line
        id = line.split('/')[-1]
        ans[int(id)] = {
            'id': int(id),
            'title': title,
            'url': line,
            'items': option
        }

print ans
