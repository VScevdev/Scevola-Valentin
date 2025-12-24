from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.validators import validate_username

User = settings.AUTH_USER_MODEL

COUNTRY_CHOICES = [
    ('AR', 'Argentina'),
    ('UY', 'Uruguay'),
    ('CL', 'Chile'),
    ('BR', 'Brasil'),
    # después se completa
]

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    # Canonical (DB / URLs)
    username = models.CharField(
        max_length=24,
        unique=True,
        editable=False,
        null=True,
        blank=True,
    )

    # Display
    username_display = models.CharField(
        max_length=24,
        validators=[validate_username],
        blank=True,
    )

    country = models.CharField(
        max_length=2,
        choices=COUNTRY_CHOICES,
        blank=True,
        null=True,
    )

    bio = models.TextField(
        max_length=300,
        blank=True
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )

    onboarding_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.username_display:
            self.username = self.username_display.strip().lower()
        else:
            self.username = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("profiles:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.username_display or self.user.email
        