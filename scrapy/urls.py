# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from scrapy import views



urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^scrapy/tb_revolution[/]+$', views.scrapy_tb_revolution, name='tb_revolution'),
    url(r'^scrapy/tb_galileo[/]+$', views.scrapy_tb_galileo, name='tb_galileo'),
    url(r'^scrapy/tb_bccampus[/]+$', views.scrapy_tb_bccampus, name='tb_bccampus'),
    url(r'^scrapy/tb_oercommons[/]+$', views.scrapy_oer_commons, name='tb_oercommons'),
]