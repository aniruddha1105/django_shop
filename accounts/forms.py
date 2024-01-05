# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username',
                  'email', 'phone_number', 'password1', 'password2']
        
        
