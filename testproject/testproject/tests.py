# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.conf import settings
from django.test.testcases import TestCase
from django.test.utils import override_settings
from js_urlresolver.templatetags.js_urlresolver import js_urlresolver_data


@override_settings(JS_URLRESOLVER_NAMES=['home', 'test'])
class Test(TestCase):
    def test_js_urlresolver_template_tag(self):
        names = getattr(settings, 'JS_URLRESOLVER_NAMES')

        data = json.loads(js_urlresolver_data())

        self.assertIn('home', data.keys())
        self.assertIn('test', data.keys())
        self.assertNotIn('test2', data.keys())

        for name in ['home', 'test']:
            self.assertEqual(
                ['test_pattern', 'replace_pattern', 'kwargs'].sort(),
                data[name].keys().sort()
            )

        data_custom_urls = json.loads(js_urlresolver_data('home, test2'))

        self.assertIn('home', data_custom_urls.keys())
        self.assertNotIn('test', data_custom_urls.keys())
        self.assertIn('test2', data_custom_urls.keys())

        for name in ['home', 'test2']:
            self.assertEqual(
                ['test_pattern', 'replace_pattern', 'kwargs'].sort(),
                data_custom_urls[name].keys().sort()
            )
