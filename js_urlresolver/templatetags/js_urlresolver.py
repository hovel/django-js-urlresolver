# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from importlib import import_module
import json
from django.conf import settings
from django.core.urlresolvers import get_urlconf, RegexURLResolver, \
    RegexURLPattern
from django.template import Library
from django.utils import six
from django.utils.regex_helper import normalize
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag()
def js_urlresolver_data(names=None):
    if names:
        if isinstance(names, six.string_types):
            names = [n.strip() for n in names.split(',')]
    else:
        names = getattr(settings, 'JS_URLRESOLVER_NAMES', [])
    names = list(set(names))

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

    urls = import_module(get_urlconf(default=settings.ROOT_URLCONF))
    walk_urlpatterns(urls.urlpatterns, ())

    return mark_safe(json.dumps(data))
