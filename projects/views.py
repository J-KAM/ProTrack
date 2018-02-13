import requests
from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, ListView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from comments.forms import CommentForm
from issues.models import Issue
from milestones.models import Milestone
from organizations.models import Organization
from projects.forms import CreateProjectForm, UpdateProjectForm
from projects.models import Project


class ProjectsPreview(ListView):
    template_name = 'projects/preview.html'
    context_object_name = 'all_projects'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user) | Project.objects.filter(collaborators=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owned_projects'] = context['all_projects'].filter(owner=self.request.user)
        context['collaborated_projects'] = context['all_projects'].filter(collaborators=self.request.user)
        return context


class ProjectCreate(CreateView):
    form_class = CreateProjectForm
    template_name='projects/project_form.html'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(None)
        form.fields['organization_owner'].queryset = Organization.objects.filter(members=request.user)
        form.fields['organization_owner'].required = False

        if request.META.get('HTTP_REFERER') is not None:
            url_path = request.META.get('HTTP_REFERER').split('/')
            if len(url_path) == 7 and url_path[3] == "organizations" and url_path[5] == "details":  # creating project in organization
                organization = Organization.objects.get(id=int(url_path[4]))
                form.initial['organization_owner'] = organization

        return render(request, self.template_name, {'form': form, 'action': 'New'})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        form.fields['organization_owner'].required = False
        error_message = ""

        if form.is_valid():
            project = form.save(commit=False)

            if form.cleaned_data['owner_type'] == 'o':
                project.organization_owner = form.cleaned_data['organization_owner']
                project.owner = None
                project.url = str(get_current_site(request)) + '/' + project.organization_owner.name + '/' + form.cleaned_data['name']

            elif form.cleaned_data['owner_type'] == 'm':
                project.organization_owner = None
                project.owner = request.user
                project.url = str(get_current_site(request)) + '/' + request.user.username + '/' + form.cleaned_data['name']

            project.created = date.today()

            try:
                project.save()
                if form.cleaned_data['owner_type'] == 'o':
                    members = Organization.objects.get(id=project.organization_owner.id).members.all()
                    for member in members:
                        project.collaborators.add(member)
                return render(request, 'projects/add_collaborators.html', {'project': project})
            except IntegrityError:
                error_message = "Entered data is not valid. Please try again."

        return render(request, 'projects/project_form.html', {'form': form, 'action': 'New', 'error_message': error_message})


class ProjectUpdate(UpdateView):
    form_class = UpdateProjectForm
    template_name = 'projects/project_form.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = Project.objects.get(id=self.kwargs['id'])
        form = self.get_form(self.form_class)
        if self.object.is_git:
            form.initial['project_type'] = 'g'
        else:
            form.initial['project_type'] = 'p'
        return render(request, self.template_name, {'form': form, 'object': self.object, 'action': 'Edit'})

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        project = Project.objects.get(id=self.kwargs['id'])
        form = self.form_class(request.POST, instance=project)
        error_message = ""

        if form.is_valid():
            try:
                project.save()
                return redirect('projects:detail', project.id)
            except IntegrityError:
                error_message = "Entered data is not valid. Please try again."

        return render(request, self.template_name, {'form': form, 'action': 'Edit', 'error_message': error_message})


class ProjectDetail(DetailView):
    model = Project
    template_name = 'projects/detail_preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = context['project']

        #get project commits
        if project.is_git:
            repo_url = 'https://api.github.com/repos/' + project.git_owner + '/' + project.git_name
            branches_url = 'https://api.github.com/repos/' + project.git_owner + '/' + project.git_name + '/branches'
            commits_url = 'https://api.github.com/repos/' + project.git_owner + '/' + project.git_name + '/commits'

            context['default_branch'] = requests.get(repo_url).json()['default_branch']
            context['branches'] = requests.get(branches_url).json()
            context['commits_data'] = requests.get(commits_url).json()

        #get project milestones
        context['project_milestones'] = Milestone.objects.filter(project=project)
        context['open_milestones'] = context['project_milestones'].filter(status="OPEN")
        context['closed_milestones'] = context['project_milestones'].filter(status="CLOSED")

        #get project issues
        issues = Issue.objects.filter(project=project)
        context['open_issues'] = issues.filter(status="Open")
        context['in_progress_issues'] = issues.filter(status="In progress")
        context['done_issues'] = issues.filter(status="Done")
        context['closed_issues'] = issues.filter(status="Closed")

        context['comment_form'] = CommentForm()
        return context


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projects:preview')


@login_required
def get_commits(request):
    selected_branch = request.GET.get('selected_branch', None)
    project_id = request.GET.get('project_id', None)

    if project_id is not None:
        project = Project.objects.get(id = project_id)
        if project.is_git:
            commits_url = 'https://api.github.com/repos/' + project.git_owner + '/' + project.git_name + '/commits?sha=' + selected_branch

    commits = requests.get(commits_url).json()
    return JsonResponse(commits, safe=False)


@login_required
def get_commit(request, pid, cid):
    project = Project.objects.get(id=pid)

    if project is not None and project.is_git:
        commit_url = 'https://api.github.com/repos/' + project.git_owner + '/' + project.git_name + '/commits/' + cid
        commit = requests.get(commit_url).json()

        commit_date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
        return render(request, 'projects/commit_detail.html', {'commit_data': commit, 'date': commit_date})

    return render(request, 'core/home_page.html')


@login_required
def remove_collaborator(request, uid, pid):
    if User.objects.filter(id=uid).exists() and Project.objects.filter(id=pid).exists():
        collaborator = User.objects.get(id=uid)
        project = Project.objects.get(id=pid)
        project.collaborators.remove(collaborator)

    return redirect('projects:detail', pid)


@login_required
def add_collaborators(request, **kwargs):
    project = Project.objects.get(id=kwargs['id'])
    return render(request, 'projects/add_collaborators.html', {'project': project})


def show_invitation(request, uidb64, pidb64):
    uid = force_text(urlsafe_base64_decode(uidb64))
    pid = force_text(urlsafe_base64_decode(pidb64))

    if User.objects.filter(id=uid).exists() and Project.objects.filter(id=pid).exists():
        project = Project.objects.get(id=pid)
        return render(request, 'projects/invitation.html', {'user_id': uid, 'project_id': pid, 'project_name': project.name, 'new': project.invited_collaborators.filter(id=uid).exists()})
    else:
        return render(request, 'core/home_page.html')


def manage_invitation(request):
    if request.method == 'POST':
        try:
            user_id = request.POST['user_id']
            project_id = request.POST['project_id']
            user = User.objects.get(id=user_id)
            project = Project.objects.get(id=project_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist, Project.DoesNotExist):
            user = None

        if user is not None and 'accept' in request.POST:
            project.invited_collaborators.remove(user)
            project.collaborators.add(user)
            project.save()
        elif user is not None and 'decline' in request.POST:
            project.invited_collaborators.remove(user)
            project.save()
        return render(request, 'core/home_page.html')


@login_required
def invite_collaborators(request):
    if request.method == 'POST':
        collaborator = request.POST.get('collaborator')
        project_id = request.POST.get('project_id')

        project = Project.objects.get(id=project_id)

        if User.objects.filter(username=collaborator).exists():
            user = User.objects.get(username=collaborator)
        elif User.objects.filter(email=collaborator).exists():
            user = User.objects.get(email=collaborator)
        else:
            user = None

        error_message = check_collaborator(user, project)
        if error_message == "":
            project.invited_collaborators.add(user)

            mail_subject = 'You have been invited to collaborate on a project'
            message = render_to_string('projects/invitation_email.html', {
                'project': project,
                'user': user,
                'domain': get_current_site(request),
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'pid': urlsafe_base64_encode(force_bytes(project.id)),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = 'html'
            email.send(fail_silently=True)

            project.save()

    return render(request, 'projects/add_collaborators.html', {'project': project, 'error_message': error_message})


def check_collaborator(user, project):
    if user is None:
        error_message = 'There is no such user. Please try again.'
        return error_message
    if user == project.owner:
        error_message = 'Owner of the project cannot be a collaborator. Please try again.'
        return error_message
    elif user in project.collaborators.all():
        error_message = 'User is already a collaborator. Please try again.'
        return error_message
    elif user in project.invited_collaborators.all():
        error_message = 'User is already invited to be a collaborator. Please try again.'
        return error_message
    return ""