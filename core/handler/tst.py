# coding=utf-8
import json

from core.handler.base import PostHandler
from core.handler.form import Form


class WBHandler(PostHandler):
    def form(self, ):
        form = Form(u"微博投票", u"投票 * 3", u"微博自动投票")

        # 分享 or 匿名
        option = Form.CheckBox(order="-")
        option.append("share", u"分享")
        option.append("niming", u"匿名")
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


print json.dumps(WBHandler().render_form(),indent=4)

print WBHandler().name