from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView

from issues.forms import IssueForm
from issues.models import Issue


class IssuePreview(generic.ListView):
    template_name = 'issues/preview.html'
    context_object_name = 'all_issues'

    def get_queryset(self):
        return Issue.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_issues'] = context['all_issues'].filter(status="Open")
        context['in_progress_issues'] = context['all_issues'].filter(status="In progress")
        context['done_issues'] = context['all_issues'].filter(status="Done")
        context['closed_issues'] = context['all_issues'].filter(status="Closed")
        return context


class IssueFormView(CreateView):
    form_class = IssueForm
    template_name = 'issues/issue_form.html'


    #display blank form
    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'action': 'New'})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            issue = form.save(commit=False)
            if issue.time_spent is None:
                issue.time_spent = 0.0
            issue.total_time_spent = issue.time_spent
            issue.save()

            if issue is not None:
                return redirect('issues:preview')

        return render(request, 'issues/issue_form.html', {'form': form, 'action': 'New'})


class IssueUpdate(UpdateView):
    form_class = IssueForm
    model = Issue
    template_name = 'issues/issue_form.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = Issue.objects.get(id=self.kwargs['id'])
        form = self.get_form(self.form_class)
        return render(request, self.template_name, {'form': form, 'object': self.object, 'action': 'Edit'})

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        issue = Issue.objects.get(id=self.kwargs['id'])
        form = self.form_class(request.POST, instance=issue)

        if form.is_valid():
            time_spent = form.cleaned_data['time_spent']
            if time_spent is None:
                time_spent = 0.0

            issue.total_time_spent = issue.total_time_spent + time_spent
            issue.time_spent = 0.0
            issue.save()

            if issue is not None:
                return redirect('issues:preview')

        return render(request, 'issues/issue_form.html', {'form': form, 'action': 'Edit'})

@login_required
def close_issue(request, **kwargs):
    issue = Issue.objects.get(id=kwargs['id'])
    issue.status = 'Closed'
    issue.save()

    return redirect('issues:preview')

@login_required
def reopen_issue(request, **kwargs):
    issue = Issue.objects.get(id=kwargs['id'])
    issue.status = 'Open'
    issue.save()

    return redirect('issues:preview')
