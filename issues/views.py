from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView

from issues.forms import IssueForm
from issues.models import Issue


class IssuePreview(generic.ListView):
    template_name = 'issues/preview.html'
    context_object_name = 'all_issues'

    def get_queryset(self):
        Issue.objects.all()


class IssueFormView(CreateView):
    form_class = IssueForm
    template_name = 'issues/issue_form.html'


    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'action': 'New'})

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

    def get_object(self, queryset=None):
        obj = Issue.objects.get(id=self.kwargs['id'])
        return obj

    def get(self, request, **kwargs):
        self.object = Issue.objects.get(id=self.kwargs['id'])
        form = self.get_form(self.form_class)
        return render(request, self.template_name, {'form': form, 'object': self.object, 'action': 'Edit'})

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
