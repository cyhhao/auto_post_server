# coding=utf-8


from core.handler.base import PostHandler
from core.handler.form import Form


class TiebaHandler(PostHandler):
    def form(self, ):
        form = Form(u"百度贴吧", u"自动签到", u"贴吧自动签到")

        return form

    def payload(self, options):
        pass

    def header(self):
        return {
            "baidu.com": {
                "Referer": "http://baidu.com",
                "Origin": "http://baidu.com"
            }
        }
