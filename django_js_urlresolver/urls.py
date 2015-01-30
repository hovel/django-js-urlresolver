# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django_js_urlresolver.views import urlreverse, urlresolve

urlpatterns = patterns('',
    url(r'^urlreverse/$', urlreverse, name='urlreverse'),
    url(r'^urlresolve/$', urlresolve, name='urlresolve'),
)
