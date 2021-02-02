from django.http import HttpResponse, JsonResponse
import json
from datetime import date, datetime
# import datetime
from django.db import models
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import make_aware

def dashboard(request):
    return render(request, 'html/dashboard/dashboard.html')

