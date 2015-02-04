# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import traceback

from django.core.exceptions import PermissionDenied
from importlib import import_module
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch, resolve, \
    Resolver404, get_urlconf
from django.http.response import JsonResponse, HttpResponse

from django.utils.six.moves.urllib.parse import urlparse


def check_permissions(viewname):
    whitelist = getattr(
        import_module(get_urlconf()), 'DJANGO_JS_URLRESOLVER_WHITELIST', []
    )
    if not whitelist or all(pattern != viewname for pattern in whitelist):
        raise PermissionDenied()


def urlreverse(request):
    try:
        urlparams = json.loads(request.body)
        viewname = urlparams.get('viewname') or urlparams.get('view_name')
        check_permissions(viewname)
        url = reverse(
            viewname=viewname,
            args=urlparams.get('args'),
            kwargs=urlparams.get('kwargs'),
        )
        return JsonResponse({'resolved': url})
    except NoReverseMatch:
        return HttpResponse('URL not found, check input parameters.')
    except Exception as e:
        if settings.DEBUG:
            return HttpResponse(traceback.format_exc())
        else:
            return HttpResponse()


def urlresolve(request):
    try:
        url = urlparse(json.loads(request.body).get('url'))
        resolver_match = resolve(url.path)
        viewname = resolver_match.view_name
        check_permissions(viewname)
        urlparams = {
            'view_name': viewname,
            'viewname': viewname,
            'args': resolver_match.args,
            'kwargs': resolver_match.kwargs,
        }
        return JsonResponse(urlparams)
    except Resolver404:
        return HttpResponse('Wrong URL, check input parameters.')
    except Exception as e:
        if settings.DEBUG:
            return HttpResponse(traceback.format_exc())
        else:
            return HttpResponse()
