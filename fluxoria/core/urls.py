from django.urls import path
from .views import home
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path("random/", views.random_post, name="random"),
    path("about_me/", views.about_me, name="about_me"),
]
