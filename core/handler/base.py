from __future__ import unicode_literals

import json

from core.helpers.data_helper import DotDict


class PostHandler:
    def __init__(self):
        self.name = self.__class__.__name__

    def form(self):
        pass

    def payload(self, options, payload_callback=None):
        pass

    def response(self, payloads):
        pass

    def header(self):
        pass

    def render_form(self):
        data = self.form().render()
        data['_key'] = self.name
        return data

    def render_payload(self):
        pass

    def render_response(self):
        pass

    def get_res(self, item):
        if item and isinstance(item, dict):
            res = item.get('res', {})
            if res.get('status') == 200:
                data = res.get('data', {})
                if not isinstance(data, dict):
                    try:
                        data = json.loads(data)
                    except:
                        data = {'code': 0, "msg": "no json"}
                res['data'] = DotDict(data)
            if 'msg' not in res:
                res['msg'] = ''
            if 'data' not in res:
                res['data'] = {}
            return DotDict(res)
        else:
            return {
                "status": 0,
                "redadyState": 0,
                "msg": "no item"
            }
