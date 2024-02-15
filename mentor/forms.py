from django import forms
from django.contrib.auth.models import User
from . import models

class mentorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class mentorForm(forms.ModelForm):
    class Meta:
        model=models.mentor
        fields=['address','mobile','profile_pic']

