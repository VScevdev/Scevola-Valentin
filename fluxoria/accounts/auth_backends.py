from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Login con:
    - email (User.email)
    - username público (Profile.username)
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        user = None

        # 1) Intentar por email
        try:
            user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            pass

        # 2) Intentar por username (Profile)
        if user is None:
            try:
                profile = Profile.objects.select_related("user").get(
                    username__iexact=username
                )
                user = profile.user
            except Profile.DoesNotExist:
                return None

        # 3) Validar password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
