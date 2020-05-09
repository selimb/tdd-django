import uuid
from unittest import mock

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from accounts.models import Token


class TestSendLoginEmail(TestCase):
    def post(self, **kwargs):
        return self.client.post(
            "/accounts/send_login_email", data={"email": "edith@example.com"}, **kwargs
        )

    def test_redirects_to_home_page(self):
        response = self.post()
        self.assertRedirects(response, "/")

    def test_sends_email(self):
        self.post()
        self.assertEqual(
            [(msg.subject, msg.to) for msg in mail.outbox],
            [("Your login link for Superlists", ["edith@example.com"],)],
        )

    def test_adds_success_message(self):
        response = self.post(follow=True,)
        self.assertEqual(
            [(msg.message, msg.tags) for msg in response.context["messages"]],
            [
                (
                    "Check your email, we've sent you a link you can use to log in.",
                    "success",
                )
            ],
        )

    def test_creates_token_associated_with_email(self):
        self.post()
        self.assertEqual([t.email for t in Token.objects.all()], ["edith@example.com"])

    def test_sends_link_to_login_using_token_uid(self):
        response = self.post()

        token = Token.objects.first()
        expected_url = response.wsgi_request.build_absolute_uri(
            f"/accounts/login?token={token.uid}"
        )
        self.assertIn(expected_url, mail.outbox[0].body)


TEST_UID = str(uuid.uuid4())


# @mock.patch("accounts.views.auth", autospec=True)
@mock.patch("accounts.views.auth")
class TestLogin(TestCase):
    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get(f"/accounts/login?token={TEST_UID}")
        self.assertRedirects(response, "/")

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get(f"/accounts/login?token={TEST_UID}")
        mock_auth.authenticate.assert_called_once_with(TEST_UID)

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get(f"/accounts/login?token={TEST_UID}")
        mock_auth.login.assert_called_once_with(
            response.wsgi_request, mock_auth.authenticate.return_value
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get(f"/accounts/login?token={TEST_UID}")
        mock_auth.login.assert_not_called()
