from django.shortcuts import render

# Create your views here.

def profile_view():
    return render(request='accounts/profile.html')