import uuid

from django.test import TestCase
from django.contrib import auth

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = auth.get_user_model()


class TestAuthenticate(TestCase):
    def test_returns_none_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(uuid.uuid4())
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = "edith@example.com"
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = "edith@example.com"
        user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        ret = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(ret, user)


class TestGetUser(TestCase):
    def test_gets_users_by_email(self):
        User.objects.create(email="another@example.com")
        desired_user = User.objects.create(email="edith@example.com")
        found_user = PasswordlessAuthenticationBackend().get_user("edith@example.com")
        self.assertEqual(found_user, desired_user)

    def test_returns_none_if_no_user_with_that_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user("edith@example.com"), None
        )
