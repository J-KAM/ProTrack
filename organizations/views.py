from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from organizations.forms import OrganizationForm


class OrganizationFormView(CreateView):
    form_class = OrganizationForm
    template_name = 'organizations/organization_form.html'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            organization = form.save(commit=False)
            organization.save()
            organization.members.add(request.user)
            return redirect('core:home')

        return render(request, 'organizations/organization_form.html', {'form': form})
