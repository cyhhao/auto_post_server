# coding=utf-8


from core.handler.base import PostHandler
from core.handler.form import Form


class BaikeHandler(PostHandler):
    def form(self, ):
        form = Form(u"百度百科", u"送花 * 3", u"每天自动送花 * 3")

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
