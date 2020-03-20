from django.urls import resolve
from django.test import TestCase
from lists.views import home_page


class TestHomePage(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        print(found)
        self.assertEqual(found.func, home_page)
