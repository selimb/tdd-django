from imbox import Imbox
import re
import time

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest, TEST_MAIL_PASSWORD, TEST_MAIL_USERNAME

SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):
    def wait_for_email(self, subject):
        if not TEST_MAIL_PASSWORD:
            email = mail.outbox[0]
            self.assertEqual(email.to, [TEST_MAIL_USERNAME])
            self.assertEqual(email.subject, subject)
            return email.body

        start = time.time()
        with Imbox(
            "imap.gmail.com",
            username=TEST_MAIL_USERNAME,
            password=TEST_MAIL_PASSWORD,
            ssl=True,
            ssl_context=None,
            starttls=False,
        ) as imbox:
            while time.time() - start < 60:
                for uid, message in imbox.messages(folder="Test", unread=True):
                    imbox.mark_seen(uid)
                    if subject in message.subject:
                        return "\n".join(message.body["plain"])
                time.sleep(5)

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.visit_home_page()
        self.browser.find_element_by_name("email").send_keys(TEST_MAIL_USERNAME)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                "Check your email", self.browser.find_element_by_tag_name("body").text
            )
        )

        # She checks her email and finds a message
        body = self.wait_for_email(SUBJECT)

        # It has a url link in it
        self.assertIn("Use this link to log in", body)
        url_search = re.search(r"http://.+/.+$", body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # she is logged in
        self.wait_to_be_logged_in(TEST_MAIL_USERNAME)

        # Now she logs out
        self.browser.find_element_by_link_text("Log out").click()

        # She is logged out
        self.wait_to_be_logged_out(TEST_MAIL_USERNAME)
