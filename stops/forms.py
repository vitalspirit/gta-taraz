from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
         model = User
         fields = ['username', 'email', 'password1', 'password2']

class SD_add_form(forms.ModelForm):
    class Meta:
        model = Shutdown
        fields = '__all__'

        widgets = {
            'sd_type': forms.Select(attrs={'class': 'form-control'}),
            'station': forms.Select(attrs={'class': 'form-control'}),
            'gtu': forms.TextInput(attrs={'class': 'form-control'}),
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'act_number': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'detailed_desc': forms.Textarea(attrs={'class': 'form-control'}),
            'sd_act': forms.FileInput(attrs={'class': 'form-control'}),

        }
