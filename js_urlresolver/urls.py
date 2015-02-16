# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from js_urlresolver.views import reverse, resolve


urlpatterns = patterns('',
    url(r'^reverse/$', reverse, name='reverse'),
    url(r'^resolve/$', resolve, name='resolve'),
)
