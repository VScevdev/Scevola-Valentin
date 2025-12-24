from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("register/", views.register_view, name="register"),
    path("onboarding/", views.onboarding_view, name="onboarding"),
    path('', include('core.urls')),
]