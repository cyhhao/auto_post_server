# coding=utf-8
import os
import requests

start = 138038048
end = 138360044
last = -1

import multiprocessing
from pyquery import PyQuery as pq

stop = {}


def get(index):
    url = 'http://vote.weibo.com/poll/%s' % index
    req = requests.get(url)
    # print req.url
    if 'passport' in req.url or 'sorry' in req.url:
        print 'out'
        with open('./stop', 'w')as f:
            f.write('1')
            f.close()

    res = req.text
    if u'大张伟' in res:
        doc = pq(req.text)
        flag = doc('.sele_but >a').text()
        if flag != u'已结束':
            print url
            with open('./ans0', 'a+') as f:
                f.write(url + '\n')
                f.close()


# req=requests.get('http://vote.weibo.com/poll/138900000')
# print req.url

# exit(0)

pool = multiprocessing.Pool(processes=10)
for index, i in enumerate(xrange(138900000, 1389000001)):
    pre = int(float(index) * 100 / (end - start))
    if pre != last:
        print pre
        last = pre

    if os.path.exists('./stop'):
        print index
        print 'break'
        break
    pool.apply_async(get, (i,))
print 'close ing'
pool.close()
print 'join ing'
pool.join()

print 'ok'
