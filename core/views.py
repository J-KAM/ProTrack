from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserForm
# Create your views here.

class UserFormView(View):
    form_class = UserForm
    template_name = 'core/registration_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user.set_password(password)
            user.save()

            if user is not None:
                print("aaa")
                return redirect('core:registration')

