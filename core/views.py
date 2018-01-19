from email.utils import unquote

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django import forms


from core.forms import ProfileForm
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

class ProfileFormView(View):
    form_class = ProfileForm
    template_name = 'core/profile_form.html'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(data=request.POST, instance=request.user)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.user.username = request.user.username
            user = User.objects.filter(email=unquote(request.user.email))

            if user:
                print(user[0].username)
                if user[0].id == request.user.id: #if user didn't change email
                    update.save()
                else:
                    return render(request, self.template_name, {'form': form,
                                                                'error_message':'This email address is already in use. Please supply a different email address.'})
            else:
                update.save()

        return render(request, self.template_name, {'form': form})
