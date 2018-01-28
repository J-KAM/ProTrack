from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from organizations.forms import OrganizationForm


class OrganizationPreview(ListView):
    template_name = 'organizations/preview.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.get(id=self.request.user.id).organization_member.all()


class OrganizationDetails(ListView):
    template_name = 'organizations/organization_details.html'
    context_object_name = 'organization'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.get(id=self.request.user.id).organization_member.get(id=self.kwargs['id'])


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
            return redirect('organizations:preview')

        return render(request, 'organizations/organization_form.html', {'form': form})
