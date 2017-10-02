# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render

# Create your views here.
from core.helpers.format_helper import FormatHelper
from dzw.handler import all_hander, all_hander_dict


def headers_config(request):
    data = {}
    for hander in all_hander:
        data.update(hander.header())

    return FormatHelper.res_format(code=200, data=data)


def main_page(request):
    data = []
    for hander in all_hander:
        print hander.render_form()
        data.append(hander.render_form())
    return FormatHelper.res_format(code=200, data=data)


def get_payload(request):
    options = request.POST.get('options')
    if options:
        options = json.loads(options)
        key = options.get('_key', '')
        extra = options.get('description', {}).get('extra', [])
        extra_options = []
        if len(extra) > 0:
            for item in extra:
                extra_options.append(item.get('ans'))
        payload_callback = None
    else:
        payload_callback = request.POST.get('payload_callback')
        payload_list = request.POST.get('payload_list')
        payload_callback = json.loads(payload_callback)
        payload_list = json.loads(payload_list)

        key = payload_callback.get('_key', '')
        extra_options = payload_list

    handler = all_hander_dict.get(key)
    if handler:
        success, payloads, callback = handler.payload(extra_options, payload_callback)
        if success:
            if not isinstance(payloads, list):
                payloads = [payloads]
            if isinstance(callback, dict):
                callback['_key'] = key
            data = {
                "payloads": payloads,
                "callback": callback,
                "_key": key
            }
            return FormatHelper.res_format(200, 'ok', data)
        else:
            return FormatHelper.res_format(400, payloads, callback)
    else:
        return FormatHelper.res_format(403, 'no such handler:' + key)


def deal_response(request):
    payloads = request.POST.get('payloads')
    key = request.POST.get('_key')
    payloads = json.loads(payloads)
    handler = all_hander_dict.get(key)
    if handler:
        flag, msg, detail = handler.response(payloads)

        return FormatHelper.res_format(flag, msg, detail)
