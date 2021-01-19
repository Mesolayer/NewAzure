from django.shortcuts import render
from engine.models import UserData

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from badgify.commands import sync_awards


# Create your views here.
@login_required(login_url=reverse_lazy('login'))
def achievements (request):
    sync_awards()
    return render(request, 'html/achievements/achievements.html')
