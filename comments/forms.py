from django import forms
from djrichtextfield.widgets import RichTextWidget

from comments.models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=RichTextWidget())

    class Meta:
        model = Comment
        fields = ['text']