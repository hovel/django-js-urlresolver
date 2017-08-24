# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils.encoding import force_text

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

local_drivers_map = {
    'firefox': webdriver.Firefox,
    'chrome': webdriver.Chrome,
}

@override_settings(DEBUG=True, JS_URLRESOLVER_NAMES=['home', 'test'])
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

    def test_js_urlresolver(self):
        self.selenium.get(self.get_url(reverse('home')))
        print(self.selenium.page_source.encode("utf-8"))
        self.selenium.execute_script('''
            window.location.href = window.JSURLResolver.reverse(
                'test', {'test_3': 13, 'test_1': 11, 'test_2': 12}
            );
        ''')
        url = self.get_url(
            reverse('test', kwargs={'test_1': 11, 'test_2': 12, 'test_3': 13})
        )
        self.wait.until(lambda sel: sel.current_url == url)

        self.selenium.execute_script('''
            var urldata = JSURLResolver.resolve(window.location.pathname);
            window.location.href = JSURLResolver.reverse(
                urldata[0], {'test_2': urldata[1]['test_2'] * 2,
                             'test_3': urldata[1]['test_3'] * 2,
                             'test_1': urldata[1]['test_1'] * 2}
            );
        ''')
        url = self.get_url(
            reverse('test', kwargs={'test_1': 22, 'test_2': 24, 'test_3': 26})
        )
        self.wait.until(lambda sel: sel.current_url == url)
