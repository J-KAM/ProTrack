import operator
from email.utils import unquote
from functools import reduce

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.generic import View

from core.forms import ProfileForm, UserUpdateForm
from issues.views import search_issues
from milestones.views import search_milestones
from organizations.views import search_organizations
from projects.views import search_projects
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
                return redirect('core:home')

        return render(request, self.template_name, {'form':form,
                                                    'error_message': 'Invalid username and/or password. Please try again.'})

class UserUpdateFormView(View):
    user_update_form_class = UserUpdateForm
    profile_form_class = ProfileForm
    template_name = 'core/profile_form.html'

    @method_decorator(login_required)
    def get(self, request):
        user_form = self.user_update_form_class(instance=request.user)
        profile_form = self.profile_form_class(instance=request.user.profile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    @method_decorator(login_required)
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


@login_required
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


def search(request):
    if request.method == 'GET':
        keywords = request.GET['q']

        if keywords:
            keywords_list = keywords.split()
            projects = search_projects(keywords_list)
            users = search_users(keywords_list)
            organizations = search_organizations(keywords_list)
            issues = search_issues(keywords_list)
            milestones = search_milestones(keywords_list)

    return render(request, 'core/search_results.html', {'users': users,
                                                        'projects': projects,
                                                        'organizations': organizations,
                                                        'issues': issues,
                                                        'milestones': milestones })


def search_users(keywords_list):
    result = User.objects.filter(
        reduce(operator.and_, (Q(username__icontains=q) for q in keywords_list)) |
        reduce(operator.or_, (Q(first_name__icontains=q) for q in keywords_list)) |
        reduce(operator.or_, (Q(last_name__icontains=q) for q in keywords_list)) |
        reduce(operator.and_, (Q(email__icontains=q) for q in keywords_list))
    )

    return result

