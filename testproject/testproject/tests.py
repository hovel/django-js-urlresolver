# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from random import randint
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils.encoding import force_text

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

local_drivers_map = {
    'firefox': webdriver.Firefox,
    'chrome': webdriver.Chrome,
}

@override_settings(DEBUG=True)
class ClientTest(StaticLiveServerTestCase):
    selenium_wait = 30
    screenshot_count = 0

    def get_url(self, url):
        return self.live_server_url + url

    def print_screen(self):
        self.screenshot_count += 1
        self.selenium.get_screenshot_as_file(
            os.path.join(
                os.environ['CIRCLE_ARTIFACTS'],
                self.selenium.capabilities['browserName'],
                force_text(self.screenshot_count)
            )
        )

    def assertDisplayed(self, element):
        self.assertTrue(element.is_displayed())

    def assertNotDisplayed(self, element):
        self.assertFalse(element.is_displayed())

    def setUp(self):
        if os.environ['SELENIUM_TEST_TYPE'] == 'local':
            self.selenium = local_drivers_map[os.environ['SELENIUM_BROWSER']]()
        else:
            raise NotImplementedError('Remote driver not configuired')
        self.selenium.implicitly_wait(self.selenium_wait)
        self.selenium.execute_script("window.resizeTo(1024, 768);")
        self.selenium.maximize_window()
        self.wait = WebDriverWait(self.selenium, self.selenium_wait)

    def tearDown(self):
        self.selenium.quit()

    def test_js_resolver(self):
        test_id = randint(0, 100)
        start_url = self.get_url(reverse('test', kwargs={'test_id': test_id}))
        self.selenium.get(start_url)
        self.selenium.execute_script('''
            $(function () {
                resolveURL(window.location.href, function (data) {
                    var urlparams = {
                        viewname: data.viewname,
                        kwargs: {
                            test_id: Math.round(data.kwargs.test_id * 2)
                        }
                    }
                    reverseURL(urlparams, function (url) {
                        window.location.href = url;
                    });
                });
            });
        ''')
        end_url = self.get_url(reverse('test', kwargs={'test_id': test_id * 2}))
        self.wait.until(lambda sel: sel.current_url == end_url)
