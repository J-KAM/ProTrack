from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from organizations.forms import OrganizationForm
from organizations.models import Organization


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
        return render(request, self.template_name, {'form': form, 'action': 'New'})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            organization = form.save(commit=False)
            organization.save()
            organization.members.add(request.user)
            return redirect('organizations:preview')

        return render(request, 'organizations/organization_form.html', {'form': form, 'action': 'New'})


class OrganizationUpdate(UpdateView):
    form_class = OrganizationForm
    model = Organization
    template_name = 'organizations/organization_form.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        self.object = Organization.objects.get(id=self.kwargs['id'])
        form = self.get_form(self.form_class)
        form.fields['name'].disabled = True
        return render(request, self.template_name, {'form': form, 'object': self.object, 'action': 'Edit'})

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        organization = Organization.objects.get(id=self.kwargs['id'])
        form = self.form_class(request.POST, instance=organization)
        form.fields['name'].disabled = True

        if form.is_valid():
            organization.save()

            if organization is not None:
                return redirect('organizations:preview')

        return render(request, 'organizations/organization_form.html', {'form': form, 'action': 'Edit'})

