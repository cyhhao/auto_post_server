# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.handler.base import PostHandler
from core.handler.form import Form


class TiebaHandler(PostHandler):
    def form(self, ):
        form = Form("百度贴吧", "自动签到", "贴吧自动签到")

        return form

    def payload(self, options, payload_callback=None):
        pass

    def header(self):
        return {
            "baidu.com": {
                "Referer": "http://baidu.com",
                "Origin": "http://baidu.com"
            }
        }
