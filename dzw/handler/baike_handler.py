# coding=utf-8

from __future__ import unicode_literals

import json

from core.handler.base import PostHandler
from core.handler.form import Form


class BaikeHandler(PostHandler):
    def form(self, ):
        form = Form("百度百科", "送花 * 3", "每天自动送花 * 3")

        return form

    def payload(self, options, payload_callback=None):
        if not payload_callback:
            url = 'https://baike.baidu.com/starflower/api/starflowerrank'
            get_data = {
                "lemmaid": "405253"
            }
            payload = {
                "url": url,
                "data": get_data,
                "method": "get",
                "key": "get_tk"
            }
            callback = {
                "step": "get_tk"
            }
            return True, payload, callback
        else:
            print options, payload_callback
            if payload_callback.get('step') == 'get_tk':
                res = self.get_res(options[0])
                if res.status == 200:
                    data = res.data
                    if data.errno == 0 and data.isLogin:
                        tk = data.tk
                        print tk
                        # 成功取到 tk
                        url = "https://baike.baidu.com/starflower/api/starflowervote"
                        get_data = {
                            "lemmaid": "405253",
                            "tk": tk
                        }
                        payload = {
                            "url": url,
                            "data": get_data,
                            "method": "get",
                            "key": "starflowervote"
                        }

                        return True, [payload] * 3, None
                    else:
                        return False, '未登录？', '请先在 baidu.com 登录帐号'
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
        msg = '送花成功'
        fail_count = 0
        for payload in payloads:
            res = self.get_res(payload)
            if res.status == 200:
                data = res.data
                if data.errno == 3:
                    detail += '未登录，请先[点击此处](http://baidu.com)登录百度帐号'
                    fail_count += 1
                elif data.errno == 0:
                    detail += '送花成功 +1'
                elif data.errno == 4:
                    detail += '今天送花已达上限'
                    fail_count += 1
                else:
                    detail += '未知错误:%s' % json.dumps(data)
                    fail_count += 1

            else:
                if res.readyStatus != 4:
                    return 'error', '网络问题，送花失败', "网络不通，请先检查网络\n"
                else:
                    return 'error', "送花失败", res.msg

            detail += '\n'
        if fail_count == len(payloads):
            type = 'error'
            msg = '送花失败'
        return type, msg, detail
