from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from projects.forms import ProjectForm


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
            project.created = date.today()
            project.owner = request.user
            project.save()
            return redirect('core:home')

        return render(request, 'projects/project_form.html', {'form': form})
