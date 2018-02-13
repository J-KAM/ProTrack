from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from comments.forms import CommentForm
from projects.models import Project


class CommentCreateView(CreateView):
    form_class = CommentForm
    template_name = 'comments/comment_form.html'

    @method_decorator(login_required)
    def get(self, request, *args):
        form = self.get_form(self.form_class)
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            resource_id = request.POST['resource_id']
            resource_type = request.POST['resource_type']

            if resource_type == 'project' and Project.objects.filter(id=resource_id).exists():
                resource = Project.objects.get(id=resource_id)

            comment.user = request.user
            comment.text = form.fields.get('text')
            comment.content_object = resource
            comment.save()

        return redirect(request.META.get('HTTP_REFERER'))
