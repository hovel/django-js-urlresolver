# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.conf import settings
from django.core.urlresolvers import get_urlconf, RegexURLResolver, \
    RegexURLPattern
from django.template import Library
from django.utils.importlib import import_module
from django.utils.regex_helper import normalize


register = Library()


@register.simple_tag()
def js_urlresolver_data():
    urls = import_module(get_urlconf())
    names = getattr(settings, 'JS_URLRESOLVER_NAMES', [])
    data = {}

    def walk_urlpatterns(obj, parents):
        if isinstance(obj, list):
            for item in obj:
                walk_urlpatterns(item, parents)
        elif isinstance(obj, RegexURLResolver):
            if obj.namespace is None:
                parents += (obj, )
                walk_urlpatterns(obj.url_patterns, parents)
        elif isinstance(obj, RegexURLPattern):
            for name in names:
                if name == obj.name:
                    pattern = '^/'
                    for parent in parents:
                        pattern += parent.regex.pattern.lstrip('^')
                    pattern += obj.regex.pattern.lstrip('^')
                    [(replace_pattern, kwargs)] = normalize(pattern)
                    test_pattern = pattern
                    for kwarg in kwargs:
                        test_pattern = test_pattern.replace(
                            '?P<{}>'.format(kwarg), ''
                        )
                    test_pattern = test_pattern.replace('\\', '\\\\')
                    data[name] = {
                        'replace_pattern': replace_pattern,
                        'test_pattern': test_pattern,
                        'kwargs': kwargs,
                    }

    walk_urlpatterns(urls.urlpatterns, ())

    return json.dumps(data)
