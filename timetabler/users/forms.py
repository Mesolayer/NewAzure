from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() #adds an email field to the form

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
