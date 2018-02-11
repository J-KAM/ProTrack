from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from activities.models import save_activity
from issues.models import Issue
from projects.models import Project
from .models import Milestone
from .forms import MilestoneForm


class MilestonesPreview(generic.ListView):
    template_name = 'milestones/preview.html'
    context_object_name = 'all_milestones'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            projects = Project.objects.filter(collaborators=self.request.user) | Project.objects.filter(owner=self.request.user)
            milestones = Milestone.objects.filter(project__in=projects)
            return milestones

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_milestones'] = context['all_milestones'].filter(status="OPEN")
        context['closed_milestones'] = context['all_milestones'].filter(status="CLOSED")
        return context


class MilestoneDetail(generic.ListView):
    template_name = 'milestones/detail_preview.html'
    context_object_name = 'all_issues'

    def get_queryset(self, **kwargs):
        if self.request.user.is_authenticated():
            try:
                milestone = Milestone.objects.get(id=self.kwargs['id'])
            except Milestone.DoesNotExist:
                raise Http404("Milestone does not exist.")
            issues = Issue.objects.filter(milestone=milestone)
            return issues

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_issues'] = context['all_issues'].filter(status="Open")
        context['in_progress_issues'] = context['all_issues'].filter(status="In progress")
        context['done_issues'] = context['all_issues'].filter(status="Done")
        context['closed_issues'] = context['all_issues'].filter(status="Closed")
        context['milestone'] = Milestone.objects.get(id=self.kwargs['id'])
        return context


class MilestoneCreateView(CreateView):
    form_class = MilestoneForm
    template_name = 'milestones/milestone_form.html'

    @method_decorator(login_required)
    def get(self, request):
        form = self.get_form(self.form_class)
        form.fields['project'].queryset = Project.objects.filter(collaborators=request.user) | Project.objects.filter(owner=request.user)
        form.fields['project'].required = True
        return render(request, self.template_name, {'form': form, 'action': 'New'})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        form.fields['project'].required = True

        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.save()
            save_activity(user=request.user, action='opened', resource=milestone)
            save_activity(user=request.user, action='added to project', resource=milestone)

            if milestone is not None:
                return redirect('milestones:preview')

        return render(request, 'milestones/milestone_form.html', {'form': form, 'action': 'New'})


class MilestoneCreateFromProjectView(CreateView):
    form_class = MilestoneForm
    template_name = 'milestones/milestone_form.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        form = self.get_form(self.form_class)
        project = Project.objects.get(id=kwargs['project_id'])
        form.fields['project'].queryset = Project.objects.filter(collaborators=request.user) | Project.objects.filter(owner=request.user)
        form.fields['project'].initial = str(project.id)
        form.fields['project'].disabled = True
        return render(request, self.template_name, {'form': form, 'action': 'New'})

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        project = Project.objects.get(id=kwargs['project_id'])
        form.fields['project'].initial = str(project.id)
        form.fields['project'].disabled = True

        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.save()
            save_activity(user=request.user, action='opened', resource=milestone)
            save_activity(user=request.user, action='added to project', resource=milestone)

            if milestone is not None:
                return redirect('milestones:preview')

        return render(request, 'milestones/milestone_form.html', {'form': form, 'action': 'New'})


class MilestoneUpdate(UpdateView):
    form_class = MilestoneForm
    template_name = 'milestones/milestone_form.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = Milestone.objects.get(id=self.kwargs['id'])
        form = self.get_form(self.form_class)
        form.fields['project'].disabled = True
        form.fields['start_date'].disabled = True
        return render(request, self.template_name, {'form': form, 'object': self.object, 'action': 'Edit'})

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        milestone = Milestone.objects.get(id=self.kwargs['id'])
        form = self.form_class(request.POST, instance=milestone)
        form.fields['project'].disabled = True
        form.fields['start_date'].disabled = True

        if form.is_valid():
            milestone.save()
            if len(form.changed_data) > 0:
                save_activity(user=request.user, action='updated', resource=milestone)

            if milestone is not None:
                return redirect('milestones:preview')

        return render(request, 'milestones/milestone_form.html', {'form': form, 'object':milestone, 'action': 'Edit'})


@method_decorator(login_required, name='dispatch')
class MilestoneDelete(DeleteView):
    model = Milestone
    success_url = reverse_lazy('milestones:preview')


@login_required
def close_milestone(request, **kwargs):
    milestone = Milestone.objects.get(id=kwargs['id'])
    milestone.status = 'CLOSED'
    milestone.save()

    save_activity(user=request.user, action='closed', resource=milestone)

    return redirect('milestones:preview')


@login_required
def reopen_milestone(request, **kwargs):
    milestone = Milestone.objects.get(id=kwargs['id'])
    milestone.status = 'OPEN'
    milestone.save()

    save_activity(user=request.user, action='reopened', resource=milestone)

    return redirect('milestones:preview')