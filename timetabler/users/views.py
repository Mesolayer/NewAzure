from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'You account has been created! You are now able to log in!')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'html/users/register.html',{'form': form})

def profile(request):
    return render(request, 'html/users/profile.html')
