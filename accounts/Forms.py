from django import forms
from .models import Account

class RegisterationForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['first_name', 'last_name', 'email', 'phone_number', 'password']
