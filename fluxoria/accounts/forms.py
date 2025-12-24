from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from profiles.models import Profile, COUNTRY_CHOICES
from .validators import validate_username

User = get_user_model()


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email")
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=24,
        validators=[validate_username]
    )
    country = forms.ChoiceField(
        label="País",
        choices=COUNTRY_CHOICES,
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado")
        return email

    def clean_username(self):
        username_display = self.cleaned_data["username"].strip()
        username_canonical = username_display.lower()

        if Profile.objects.filter(username=username_canonical).exists():
            raise ValidationError("Este nombre de usuario ya está en uso")
        
        return username_display

    def clean(self):
        cleaned = super().clean()

        if cleaned.get("password1") != cleaned.get("password2"):
            raise ValidationError("Las contraseñas no coinciden")
        
        return cleaned
