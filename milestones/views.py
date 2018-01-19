from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView
from .models import Milestone
from .forms import MilestoneForm


# def preview(request):
#     return render(request, 'core/home_page.html')


class preview(generic.ListView):
    template_name = 'milestones/preview.html'
    context_object_name = 'all_milestones'

    def get_queryset(self):
        return Milestone.objects.all()


class MilestoneFormView(View):
    form_class = MilestoneForm
    template_name = 'milestones/milestone_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.total_progress = 0
            milestone.total_time_spent = 0.0
            milestone.save()
            return redirect('milestones:preview')

        return render(request, 'milestones/milestone_form.html', {'form': form})


class MilestoneCreate(CreateView):
    model = Milestone
    fields = ['name', 'description', 'start_date', 'due_date']