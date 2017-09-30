# coding=utf-8
import json

from core.handler.base import PostHandler
from core.handler.form import Form


class WeiboHandler(PostHandler):
    def form(self):
        form = Form(u"微博投票", u"投票 * 3", u"微博自动投票")

        # 分享 or 匿名
        option = Form.CheckBox(order="-")
        option.append("share", u"分享")
        option.append("anonymous", u"匿名")
        option.default = ['share']
        form.append_extra(option)

        # 选择哪个投票
        votes = Form.CheckBox()
        for i in xrange(12345, 12349):
            votes.append(i, "投票 id " + str(i))
            votes.default.append(i)
        form.append_extra(votes)

        # 单选男歌手女歌手
        select = Form.Radio(default="man")
        select.append("man", u"男歌手", "http://weibo.com")
        select.append("woman", u"女歌手", "http://weibo.com")
        form.append_extra(select)

        return form

    def payload(self, options):
        # 这里的 options 对应了上面的每项表单
        option = options[0]
        votes = options[1]
        select = options[2]

        print option, votes

        payloads = []
        for vote in votes:
            url = "http://vote.weibo.com/aj/joinpoll?ajwvr=6&__rnd=1506586072256"
            post_data = {
                "poll_id": str(vote),
                "items": 20,
                "anonymous": 1 if 'anonymous' in option else 0,
                "share": 1 if 'share' in option else 0,
                "_t": 0
            }
            payloads.append({
                "key": vote,
                "url": url,
                "data": post_data,
                "method": "post"
            })

        return payloads

    def header(self):
        return {
            "vote.weibo.com": {
                "Referer": "http://vote.weibo.com",
                "Origin": "http://vote.weibo.com"
            }
        }

    def response(self, payloads):
        detail = u""
        type = 'success'
        msg = u'投票成功'

        for payload in payloads:
            res = payload.get('res')
            # res 格式：
            # 成功：{
            #     status: 200,
            #     data: 请求返回的数据
            # }
            # 失败：{
            #     status: http状态码
            #     readyState: ajax 的 readyState
            #     msg: 错误信息
            # }
            if res.get('code') == 200:
                data = res.get('data')
                data = json.loads(data)
                # todo 做一些判断，可以添加每个请求成功与否的信息，例如：
                detail = u"""
                    12345这个投票成功了
                    12346这个投票失败了，请点击[链接](http://weibo.com)查看详情               
                    12346这个投票失败了，因为你没登录，请点击[链接](http://weibo.com)先完成登录
                """
            else:
                type = 'error'
                msg = u"投票失败"
        return type, msg, detail
