from django.shortcuts import redirect
from django.urls import reverse


class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            profile = getattr(request.user, "profile", None)

            if (
                profile
                and not profile.onboarding_completed
                and not request.path.startswith("/accounts/onboarding")
                and not request.path.startswith("/accounts/logout")
            ):
                return redirect("accounts:onboarding")

        return self.get_response(request)