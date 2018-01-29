from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from organizations.forms import OrganizationForm
from organizations.models import Organization


class OrganizationPreview(ListView):
    template_name = 'organizations/preview.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.get(id=self.request.user.id).members.all()


class OrganizationDetails(ListView):
    template_name = 'organizations/organization_details.html'
    context_object_name = 'organization'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.get(id=self.request.user.id).members.get(id=self.kwargs['id'])


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
            organization.owner = request.user
            organization.save()
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


class OrganizationDelete(DeleteView):
    model = Organization
    success_url = reverse_lazy('organizations:preview')


@login_required
def remove_member_from_organization(request, **kwargs):
    organization = Organization.objects.get(id=kwargs['id_org'])
    member = User.objects.get(id=kwargs['id_mem'])
    organization.members.remove(member)
    if organization.members.count() == 1 and member.id != organization.owner.id:
        return redirect('organizations:preview')

    return redirect('organizations:details', id=organization.id)


@login_required
def add_members(request, **kwargs):
    organization = Organization.objects.get(id=kwargs['id'])
    return render(request, 'organizations/add_member.html', {'organization': organization})


def show_invitation(request, uidb64, oidb64):
    uid = force_text(urlsafe_base64_decode(uidb64))
    oid = force_text(urlsafe_base64_decode(oidb64))

    if User.objects.filter(id=uid).exists() and Organization.objects.filter(id=oid).exists():
        organization = Organization.objects.get(id=oid)
        return render(request, 'organizations/invitation.html', {'user_id': uid, 'organization_id': oid,
                                                                 'organization_name': organization.name, 'new': organization.invited_members.filter(id=uid).exists()})
    else:
        return render(request, 'core/home_page.html')


def manage_invitation(request):
    if request.method == 'POST':
        try:
            user_id = request.POST['user_id']
            organization_id = request.POST['organization_id']
            user = User.objects.get(id=user_id)
            organization = Organization.objects.get(id=organization_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist, Organization.DoesNotExist):
            user = None

        if user is not None and 'accept' in request.POST:
            organization.invited_members.remove(user)
            organization.members.add(user)
            organization.save()
        elif user is not None and 'decline' in request.POST:
            organization.invited_members.remove(user)
            organization.save()
        return render(request, 'core/home_page.html')


@login_required
def invite_members(request):
    if request.method == 'POST':

        member = request.POST.get('member')
        organization_id = request.POST.get('organization_id')

        organization = Organization.objects.get(id=organization_id)

        if User.objects.filter(username=member).exists():
            user = User.objects.get(username=member)
        elif User.objects.filter(email=member).exists():
            user = User.objects.get(email=member)
        else:
            user = None

        error_message = check_member(user, organization)
        if error_message == "":
            organization.invited_members.add(user)

            mail_subject = 'You have been invited to join in organization.'
            message = render_to_string('organizations/invitation_email.html', {
                'organization': organization,
                'user': user,
                'domain': get_current_site(request),
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'oid': urlsafe_base64_encode(force_bytes(organization.id)),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = 'html'
            email.send(fail_silently=True)

            organization.save()

    return render(request, 'organizations/add_member.html', {'organization': organization, 'error_message': error_message})


def check_member(user, organization):
    if user is None:
        error_message = 'There is no such user. Please try again.'
        return error_message
    if user == organization.owner:
        error_message = 'Owner of the organization is already a member. Please try again.'
        return error_message
    elif user in organization.members.all():
        error_message = 'User is already a member. Please try again.'
        return error_message
    elif user in organization.invited_members.all():
        error_message = 'User is already invited to be a member. Please try again.'
        return error_message
    return ""

