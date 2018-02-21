from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from comments.forms import CommentForm
from comments.models import Comment
from issues.models import Issue
from milestones.models import Milestone

@login_required
def comment_create(request):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            resource_id = request.POST['resource_id']
            resource_type = request.POST['resource_type']

            if resource_type == 'issue' and Issue.objects.filter(id=resource_id).exists():
                resource = Issue.objects.get(id=resource_id)

            elif resource_type == 'milestone' and Milestone.objects.filter(id=resource_id).exists():
                resource = Milestone.objects.get(id=resource_id)

            elif resource_type == 'comment' and Comment.objects.filter(id=resource_id).exists():
                resource = Comment.objects.get(id=resource_id)

            else:
                return redirect(request.META.get('HTTP_REFERER'))

            comment.user = request.user
            comment.text = form.cleaned_data['text']
            comment.content_object = resource
            comment.save()

        return redirect(request.META.get('HTTP_REFERER'))

@login_required
def comment_update(request):
    if request.method == "POST":
        comment_id = request.POST['update_comment_id']
        comment = Comment.objects.get(id=comment_id)
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            if comment.user == request.user:
                comment.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def comment_delete(request, comment_id):
    if Comment.objects.filter(id=comment_id).exists():
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()

    return redirect(request.META.get('HTTP_REFERER'))
