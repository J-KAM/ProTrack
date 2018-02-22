from django.test import TestCase

from comments.forms import CommentForm


class CommentFormTest(TestCase):

    def test_field_labels(self):
        form = CommentForm()

        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'Text')

    def test_required_fields(self):
        form = CommentForm()

        self.assertTrue(form.fields['text'].required)

    def test_field_number(self):
        form = CommentForm()

        self.assertEquals(len(form.fields), 1)

