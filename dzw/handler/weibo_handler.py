# coding=utf-8
from __future__ import unicode_literals

import json
from core.handler.base import PostHandler
from core.handler.form import Form
from dzw.payload_data.weibo import weibo_data


class WeiboHandler(PostHandler):
    def form(self):
        form = Form("微博投票", "投票 * 3", "微博自动投票")

        # 分享 or 匿名
        option = Form.CheckBox(order="-")
        option.append_item("share", "分享")
        option.append_item("anonymous", "匿名")
        option.default = ['share']
        form.append_extra(option)

        # 选择哪个投票
        votes = Form.CheckBox()
        for id, item in weibo_data.iteritems():
            votes.append_item(item['id'], item['title'], item['url'])
            votes.default.append(item['id'])
        form.append_extra(votes)

        # 单选男歌手女歌手
        # select = Form.Radio(default="man")
        # select.append_item("man", "男歌手", "http://weibo.com")
        # select.append_item("woman", "女歌手", "http://weibo.com")
        # form.append_extra(select)

        return form

    def payload(self, options, payload_callback=None):
        # 这里的 options 对应了上面的每项表单
        option = options[0]
        votes = options[1]
        # select = options[2]

        print option, votes

        payloads = []
        for vote in votes:
            url = "http://vote.weibo.com/aj/joinpoll?ajwvr=6&__rnd=1506586072256"
            post_data = {
                "poll_id": str(vote),
                "items": int(weibo_data.get(int(vote), {}).get('items')),
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

        success = True
        callback = None
        return success, payloads, callback

    def header(self):
        return {
            "vote.weibo.com": {
                "Referer": "http://vote.weibo.com",
                "Origin": "http://vote.weibo.com"
            }
        }

    def response(self, payloads):
        detail = ""
        type = 'success'
        msg = '投票成功'

        fail_count = 0
        for payload in payloads:
            res = self.get_res(payload)
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
            vote_url = weibo_data.get(int(payload['key']), {}).get('url', '')
            vote_msg = "[->](%s)" % vote_url
            if res.status == 200:
                data = res.data

                # todo 做一些判断，可以添加每个请求成功与否的信息，例如：
                if data.code == '100000':  # 成功
                    detail += data.msg
                else:
                    if data.code == 'D00001':
                        fail_count += 1
                        detail = "您尚未登录，请先[点此登录](http://weibo.com)后，再重试"
                        return 'error', '您尚未登录，请先登录', detail
                    elif data.code == '100001':
                        fail_count += 1
                        detail += data.msg + vote_msg
                    else:
                        fail_count += 1
                        detail += data.msg + vote_msg

            else:
                if res.readyStatus != 4:
                    return 'error', '网络问题，投票失败', "网络不通，请先检查网络\n"
                else:
                    return 'error', "投票失败", res.msg + vote_msg
            detail += '\n'

        if fail_count == len(payloads):
            type = 'error'
            msg = '投票失败'
        elif fail_count > 0:
            type = 'warning'
            msg = '部分投票有问题'

        return type, msg, detail
