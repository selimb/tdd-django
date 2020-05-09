from .models import User, Token


class PasswordlessAuthenticationBackend:
    def authenticate(self, uid):
        try:
            token = Token.objects.get(uid=uid)
        except Token.DoesNotExist:
            return None
        try:
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
