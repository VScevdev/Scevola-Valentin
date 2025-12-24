from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from profiles.models import Profile, COUNTRY_CHOICES

User = get_user_model()



def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=identifier,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('core:home')

        return render(request, 'accounts/login.html', {
            'error': 'Email/Usuario y/o contraseña incorrectos'
        })

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('core:home')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username_display = form.cleaned_data["username"].strip()
            username_canonical = username_display.lower()

            # 🔒 chequeo ANTES de crear el user
            if Profile.objects.filter(username=username_canonical).exists():
                form.add_error("username", "Ese nombre de usuario ya está en uso.")
                return render(request, "accounts/register.html", {"form": form})

            user = User.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"]
            )

            profile = user.profile
            profile.username_display = username_display
            profile.country = form.cleaned_data["country"]
            profile.onboarding_completed = True
            profile.save()

            user = authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password1"]
            )

            login(request, user)
            return redirect("core:home")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})



@login_required
def onboarding_view(request):
    profile = request.user.profile

    # 🔒 si ya completó onboarding → afuera
    if profile.onboarding_completed:
        return redirect("core:home")

    if request.method == "POST":
        username_display = request.POST.get("username", "").strip()
        country = request.POST.get("country")

        if not username_display or not country:
            messages.error(request, "Completa todos los campos.")
        else:
            username_canonical = username_display.lower()

            # 🔎 chequeo contra canonical
            if Profile.objects.filter(
                username=username_canonical
            ).exclude(pk=profile.pk).exists():
                messages.error(request, "Ese username ya está en uso.")
            else:
                try:
                    profile.username_display = username_display
                    profile.country = country
                    profile.onboarding_completed = True
                    profile.save()
                    return redirect("core:home")
                
                except IntegrityError:
                    # fallback defensivo (race condition)
                    messages.error(request, "Ese username ya está en uso.")
                    
    return render(
        request,
        "accounts/onboarding.html",
        {
            "profile": profile,
            "country_choices": COUNTRY_CHOICES,
        }
    )

