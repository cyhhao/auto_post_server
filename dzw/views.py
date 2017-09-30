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
    options = json.loads(options)
    key = options.get('key', '')
    handler = all_hander_dict.get(key)
    if handler:
        extra = options.get('description', {}).get('extra', [])
        print
        extra_options = []
        if len(extra) > 0:
            for item in extra:
                extra_options.append(item.get('ans'))

        payloads = handler.payload(extra_options)

        return FormatHelper.res_format(200, data={
            "payloads": payloads,
            "key": key
        })


def deal_response(request):
    payloads = request.POST.get('payloads')
    key = request.POST.get('key')
    payloads = json.loads(payloads)
    handler = all_hander_dict.get(key)
    if handler:
        handler.response(payloads)