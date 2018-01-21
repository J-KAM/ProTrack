from email.utils import unquote

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.views.generic import View
from django import forms


from core.forms import ProfileForm, UserUpdateForm
from .forms import UserForm, SignInForm


class UserFormView(View):
    form_class = UserForm
    template_name = 'core/registration_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user.set_password(password)
            user.save()

            if user is not None:
                return redirect('core:sign_in')

        return render(request, 'core/registration_form.html', {'form': form})


class SignInFormView(View):
    form_class = SignInForm
    template_name = 'core/signin_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'error_message': ''})

    def post(self, request):
        form = self.form_class(None)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'core/home_page.html', None)

        return render(request, self.template_name, {'form':form, 'error_message': 'Invalid username and/or password. Please try again.'})


def home(request):
    return render(request, "core/home_page.html")

class UserUpdateFormView(View):
    user_update_form_class = UserUpdateForm
    profile_form_class = ProfileForm
    template_name = 'core/profile_form.html'

    def get(self, request):
        user_form = self.user_update_form_class(instance=request.user)
        profile_form = self.profile_form_class(instance=request.user.profile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):

        user_form = self.user_update_form_class(data=request.POST, instance=request.user)
        profile_form = self.profile_form_class(data=request.POST, files=request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            update = user_form.save(commit=False)
            update.user = request.user
            update.user.username = request.user.username
            user = User.objects.filter(email=unquote(request.user.email))

            if user:
                if user[0].id == request.user.id: #if user didn't change email
                    update.save()
                    profile_form.save()
                else:
                    return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form,
                                                                'error_message':'This email address is already in use. Please supply a different email address.'})
            else:
                update.save()
                profile_form.save()

        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

def change_password(request):

    if request.method == 'POST':

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!',)
            return redirect('core:change_password')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/change_password.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile picture was successfully updated.')
            return redirect('settings:profile') #or core:profile
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'core/profile_form.html', {'profile_form': profile_form})
