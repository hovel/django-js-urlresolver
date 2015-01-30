# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch, resolve, \
    Resolver404
from django.http.response import JsonResponse, HttpResponse

from django.utils.six.moves.urllib.parse import urlparse


def urlreverse(request):
    try:
        urlparams = json.loads(request.body)
        url = reverse(
            viewname=urlparams.get('viewname'),
            # urlconf=urlparams.get('urlconf'),
            args=urlparams.get('args'),
            kwargs=urlparams.get('kwargs'),
            # prefix=urlparams.get('prefix'),
            # current_app=urlparams.get('current_app')
        )
        return JsonResponse({'resolved': url})
    except NoReverseMatch:
        return HttpResponse('URL not found, check input parameters.')
    except Exception as e:
        if settings.DEBUG:
            return HttpResponse(e.message)
        else:
            return HttpResponse()


def urlresolve(request):
    # TODO white/black lists
    try:
        url = urlparse(json.loads(request.body).get('url'))
        resolver_match = resolve(url.path)
        urlparams = {
            # 'func': resolver_match.func,
            'args': resolver_match.args,
            'kwargs': resolver_match.kwargs,
            # 'url_name': resolver_match.url_name,
            # 'app_name': resolver_match.app_name,
            # 'namespace': resolver_match.namespace,
            # 'namespaces': resolver_match.namespaces,
            'view_name': resolver_match.view_name
        }
        return JsonResponse(urlparams)
    except Resolver404:
        return HttpResponse('Wrong URL, check input parameters.')
    except Exception as e:
        if settings.DEBUG:
            return HttpResponse(e.message)
        else:
            return HttpResponse()
