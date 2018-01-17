from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']