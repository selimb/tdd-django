import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from .server_tools import reset_database

MAX_WAIT = 3

STAGING_SERVER = os.getenv("STAGING_SERVER")
TEST_MAIL_USERNAME = "selim.belhaouane+testing@gmail.com"
TEST_MAIL_PASSWORD = ""
if STAGING_SERVER:
    TEST_MAIL_PASSWORD = os.environ["TEST_MAIL_PASSWORD"]


def wait(fn):
    def wrapped(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.1)

    return wrapped


class FunctionalTest(StaticLiveServerTestCase):
    @staticmethod
    def _mk_browser():
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(options=options)

    def setUp(self):
        self.browser = self._mk_browser()
        if STAGING_SERVER:
            self.live_server_url = "http://" + STAGING_SERVER
            reset_database(STAGING_SERVER)

    def tearDown(self):
        self.browser.quit()

    def visit_home_page(self):
        self.browser.get(self.live_server_url)

    def get_item_input_box(self):
        return self.browser.find_element_by_id("id_text")

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
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

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text("Log out")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name("email")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)
