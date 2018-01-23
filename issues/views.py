from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic, View
from django.views.generic import View


from issues.forms import IssueForm
from issues.models import Issue


class IssuePreview(generic.ListView):
    template_name = 'issues/preview.html'
    context_object_name = 'all_issues'

    def get_queryset(self):
        Issue.objects.all()

class IssueFormView(View):
    form_class = IssueForm
    template_name = 'issues/issue_form.html'


    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

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

        return render(request, 'issues/issue_form.html', {'form': form})
