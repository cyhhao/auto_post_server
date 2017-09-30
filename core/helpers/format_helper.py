import json
from django.http import HttpResponse


class FormatHelper:
    @classmethod
    def res_format(cls, code=200, msg='', data=None):
        return HttpResponse(json.dumps({
            'code': code,
            'msg': msg,
            'data': data
        }), content_type="application/json")

    @classmethod
    def tojson(cls, obj):
        return json.dumps(obj)
