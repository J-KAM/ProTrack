from . models import Milestone
from django import forms
from functools import partial


class MilestoneForm(forms.ModelForm):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})
    start_date = forms.DateField(widget=DateInput())
    due_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Milestone
        fields = ['name', 'description', 'start_date', 'due_date']