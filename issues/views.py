from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from issues.forms import IssueForm
from issues.models import Issue
from milestones.models import Milestone
from projects.models import Project


class IssuePreview(generic.ListView):
    template_name = 'issues/preview.html'
    context_object_name = 'all_issues'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            projects = Project.objects.filter(collaborators=self.request.user) | Project.objects.filter(
                owner=self.request.user)
            issues = Issue.objects.filter(project__in=projects)

            if self.request.path == '/issues/all/':
                return issues
            else:  # assigned
                issues = Issue.objects.filter(project__in=projects, assignees=self.request.user)
                return issues

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_issues'] = context['all_issues'].filter(status="Open")
        context['in_progress_issues'] = context['all_issues'].filter(status="In progress")
        context['done_issues'] = context['all_issues'].filter(status="Done")
        context['closed_issues'] = context['all_issues'].filter(status="Closed")
        return context


class IssueDetails(ListView):
    template_name = 'issues/issue_details.html'
    context_object_name = 'issue'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Issue.objects.get(id=self.kwargs['id'])


class IssueFormView(CreateView):
    form_class = IssueForm
    template_name = 'issues/issue_form.html'

    # display blank form
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        form = self.form_class(None)
        project = Project.objects.get(id=kwargs['project_id'])
        form.fields['milestone'].queryset = Milestone.objects.filter(project=project)
        if project.owner is not None:
            form.fields['assignees'].queryset = User.objects.filter(id=project.owner.id) | project.collaborators.all()
        else:
            form.fields['assignees'].queryset = project.collaborators.all()

        form.fields['milestone'].required = False
        form.fields['assignees'].required = False

        return render(request, self.template_name, {'form': form, 'action': 'New'})

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        form.fields['milestone'].required = False
        form.fields['assignees'].required = False

        if form.is_valid():
            issue = form.save(commit=False)
            project = Project.objects.get(id=kwargs['project_id'])
            issue.project = project
            if issue.time_spent is None:
                issue.time_spent = 0.0
            issue.total_time_spent = issue.time_spent

            issue.save()

            issue.assignees = form.cleaned_data['assignees']
            issue.save()

            milestone = issue.milestone

            if milestone is not None:
                milestone.total_time_spent = milestone.total_time_spent + issue.total_time_spent
                num_of_issues = Issue.objects.filter(milestone=milestone).count()
                issue_progress = int(issue.progress.split('%')[0])
                milestone.total_progress = (milestone.total_progress + issue_progress) / num_of_issues
                milestone.save()

            if issue is not None:
                return redirect('issues:preview_all')

        return render(request, 'issues/issue_form.html', {'form': form, 'action': 'New'})


class IssueUpdate(UpdateView):
    form_class = IssueForm
    model = Issue
    template_name = 'issues/issue_form.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = Issue.objects.get(id=self.kwargs['id'])
        form = self.get_form(self.form_class)
        form.fields['milestone'].queryset = Milestone.objects.filter(project=self.object.project)
        if self.object.project.owner is not None:
            form.fields['assignees'].queryset = User.objects.filter(id=self.object.project.owner.id) | self.object.project.collaborators.all()
        else:
            form.fields['assignees'].queryset = self.object.project.collaborators.all()

        form.fields['milestone'].required = False
        form.fields['assignees'].required = False
        return render(request, self.template_name, {'form': form, 'object': self.object, 'action': 'Edit'})

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        issue = Issue.objects.get(id=self.kwargs['id'])
        form = self.form_class(request.POST, instance=issue)
        form.fields['milestone'].required = False
        form.fields['assignees'].required = False

        if form.is_valid():
            time_spent = form.cleaned_data['time_spent']
            if time_spent is None:
                time_spent = 0.0

            issue.total_time_spent = issue.total_time_spent + time_spent
            issue.time_spent = 0.0
            issue.save()

            issue.assignees = form.cleaned_data['assignees']
            issue.save()

            milestone = issue.milestone

            if milestone is not None:
                milestone.total_time_spent = milestone.total_time_spent + issue.total_time_spent
                num_of_issues = Issue.objects.filter(milestone=milestone).count()
                issue_progress = int(issue.progress.split('%')[0])
                milestone.total_progress = (milestone.total_progress + issue_progress) / num_of_issues
                milestone.save()

            if issue is not None:
                return redirect('issues:preview_all')

        return render(request, 'issues/issue_form.html', {'form': form, 'action': 'Edit'})


@login_required
def close_issue(request, **kwargs):
    issue = Issue.objects.get(id=kwargs['id'])
    issue.status = 'Closed'
    issue.save()

    return redirect("issues:preview_all")


@login_required
def reopen_issue(request, **kwargs):
    issue = Issue.objects.get(id=kwargs['id'])
    issue.status = 'Open'
    issue.save()

    return redirect("issues:preview_all")


@login_required
def remove_assignment(request, **kwargs):
    issue = Issue.objects.get(id=kwargs['iid'])
    assignee = User.objects.get(id=kwargs['uid'])
    issue.assignees.remove(assignee)

    return redirect('issues:details', id=issue.id)
