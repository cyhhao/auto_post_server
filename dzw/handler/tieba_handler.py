# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re

from core.handler.base import PostHandler
from core.handler.form import Form


class TiebaHandler(PostHandler):
    def form(self, ):
        form = Form("百度贴吧", "签到", "大张伟吧、花儿乐队吧，自动签到")

        return form

    def payload(self, options, payload_callback=None):
        if not payload_callback:
            url = "https://tieba.baidu.com/f?ie=utf-8"
            get_data = {
                "kw": "大张伟"
            }
            payload = {
                "url": url,
                "method": "get",
                "data": get_data,
            }
            callback = {
                "step": "get_tbs"
            }
            return True, payload, callback
        else:
            print options, payload_callback
            if payload_callback.get('step') == 'get_tbs':
                res = self.get_res(options[0])
                if res.status == 200:
                    data = res.data
                    print data
                    pattern = re.compile(r"'tbs':\s*\"(.+?)\"")

                    mat = pattern.findall(data)
                    if len(mat) == 0:
                        return False, "未登录百度", "请先访问百度然后登录"
                    else:
                        tbs = mat[0]
                        payloads = []
                        callback = None
                        for kw in ["大张伟", "花儿乐队"]:
                            url = "https://tieba.baidu.com/sign/add"
                            post_data = {
                                "ie": "utf-8",
                                "kw": kw,
                                "tbs": tbs,
                            }
                            payload = {
                                "url": url,
                                "data": post_data,
                                "method": "post",
                                "name": kw
                            }
                            payloads.append(payload)
                        return True, payloads, callback

                else:
                    return False, "请检查网络链接" + res.msg, None

    def header(self):
        return {
            "baidu.com": {
                "Referer": "http://baidu.com",
                "Origin": "http://baidu.com"
            }
        }

    def response(self, payloads):
        detail = ""
        type = 'success'
        msg = '签到成功'
        fail_count = 0
        for payload in payloads:
            res = self.get_res(payload)
            ba_name = "【" + payload.get('name', '') + "】吧"
            if res.status == 200:
                data = res.data
                if data.no == 0:
                    detail += ba_name + "签到成功"
                elif data.no == 1101:
                    detail += ba_name + data.error
                    fail_count += 1
                elif data.no == 1990055:
                    detail += "未登录，请先[点击此处](https://passport.baidu.com/v2/?login)登录百度帐号"
                    fail_count += 1
                else:
                    detail += '未知错误:%s' % json.dumps(data)
                    fail_count += 1
            else:
                if res.readyStatus != 4:
                    return 'error', '网络问题，签到失败', "网络不通，请先检查网络\n"
                else:
                    return 'error', "送花失败", res.msg
            detail += '\n'
        if fail_count == len(payloads):
            type = 'error'
            msg = '签到失败'
        return type, msg, detail
