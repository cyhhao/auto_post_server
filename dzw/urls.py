from django.conf.urls import url

from dzw.views import *

urlpatterns = [
    url(r'^headers_config', headers_config),
    url(r'^main_page', main_page),
    url(r'^get_payload', get_payload),
    url(r'^deal_response', deal_response),
]
