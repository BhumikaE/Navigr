from django.contrib.auth.models import User
from django import forms
from django.db import models
from music.models import Lists

from music.models import Notification

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username','email','password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={'placeholder': 'Password'}),
            'email': forms.TextInput(attrs={'placeholder': 'E-Mail'}),
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = Lists
        fields = ['task']


class NotifyForm(forms.ModelForm):

    class Meta:

        model = Notification
        fields = ['store_latitude','store_longitude','store_name']