from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView

from projects.forms import ProjectForm
from projects.models import Project


class ProjectCreate(CreateView):
    form_class = ProjectForm
    template_name='projects/project_form.html'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.url = str(get_current_site(request)) + '/' + request.user.username + '/' + form.cleaned_data['name']
            project.created = date.today()
            project.owner = request.user
            try:
                project.save()
                return render(request, 'projects/add_collaborators.html', {'project': project})
            except IntegrityError:
                error_message = "Entered data is not valid. Please try again."

        return render(request, 'projects/project_form.html', {'form': form, 'error_message': error_message})


@login_required
def add_collaborators(request):
    return render(request, 'projects/add_collaborators.html')


@login_required
def accept_invitation(request, uidb64, pidb64, token):
    try:

        uid = force_text(urlsafe_base64_decode(uidb64))
        pid = force_text(urlsafe_base64_decode(pidb64))
        user = User.objects.get(id=uid)
        project = Project.objects.get(id=pid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, Project.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        project.invited_collaborators.remove(user)
        project.collaborators.add(user)
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
        if error_message is not None:
            project.invited_collaborators.add(user)

            # mail_subject = 'You have been invited to collaborate on a project'
            # message = render_to_string('projects/acc_active_email.html', {
            #     'project': project,
            #     'user': user,
            #     'domain': get_current_site(request),
            #     'uid': urlsafe_base64_encode(force_bytes(user.id)),
            #     'pid': urlsafe_base64_encode(force_bytes(project.id)),
            #     'token': default_token_generator.make_token(user)
            # })
            # email = EmailMessage(mail_subject, message, to=[user.email])
            # email.content_subtype = 'html'
            # email.send(fail_silently=True)

            project.save()

    return render(request, 'projects/add_collaborators.html', {'project': project, 'error_message': error_message})


def check_collaborator(user, project):
    if user is None:
        error_message = 'There is no such user. Please try again.'
        return error_message
    if user == project.owner:
        error_message = 'Owner of the project cannot be a collaborator. Please try again.'
        return error_message
    elif user in project.collaborators:
        error_message = 'User is already a collaborator. Please try again.'
        return error_message
    elif user in project.invited_collaborators:
        error_message = 'User is already invited to be a collaborator. Please try again.'
        return error_message
    return None
