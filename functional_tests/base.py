import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

STAGING_SERVER = os.environ.get("STAGING_SERVER")
MAX_WAIT = 3


class FunctionalTest(StaticLiveServerTestCase):
    @staticmethod
    def _mk_browser():
        return webdriver.Firefox()

    def setUp(self):
        self.browser = self._mk_browser()
        if STAGING_SERVER:
            self.live_server_url = "http://" + STAGING_SERVER

    def tearDown(self):
        self.browser.quit()

    def visit_home_page(self):
        self.browser.get(self.live_server_url)

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.1)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.1)
