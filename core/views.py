from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
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