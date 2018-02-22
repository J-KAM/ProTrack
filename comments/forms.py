from django import forms
from tinymce.widgets import TinyMCE

from comments.models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=TinyMCE())

    class Meta:
        model = Comment
        fields = ['text']