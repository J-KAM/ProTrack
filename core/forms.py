from django.contrib.auth.models import User
from django import forms

from core.models import Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    error_messages = {
        'duplicate_username': 'A user with that Username already exists.',
        'duplicate_email': 'This email address is already in use. Please supply a different email address.'
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User._default_manager.get(username=username)

            #if the user exists, then raise an error message
            raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',  # set the error message key

            )
        except User.DoesNotExist:
            return username

    def clean_email(self):
            email = self.cleaned_data['email']

            if email and User.objects.filter(email=email).count():
                # if the email exists, then raise an error message
                raise forms.ValidationError(
                    self.error_messages['duplicate_email'],
                    code='duplicate_email',  # set the error message key

                )
            return email


class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(widget=forms.EmailInput)

    error_messages = {
        'duplicate_email': 'This email address is already in use. Please supply a different email address.'
    }
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(label='Choose new profile image',widget=forms.FileInput, required=False)
    class Meta:
        model = Profile
        fields = ['profile_picture']