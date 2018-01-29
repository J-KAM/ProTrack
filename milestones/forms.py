from datetime import date

from . models import Milestone
from django import forms
from functools import partial


class MilestoneForm(forms.ModelForm):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})
    start_date = forms.DateField(widget=DateInput(format='%m/%d/%Y'),initial=date.today)
    due_date = forms.DateField(widget=DateInput(format='%m/%d/%Y'),initial=date.today)

    error_messages = {
        'past_start': 'Start date cannot be in the past.',
        'due_before_start': 'Due date cannot be before start date.'
    }

    class Meta:
        model = Milestone
        fields = ['name', 'project', 'start_date', 'due_date', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none;'}),
            }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < date.today():
            raise forms.ValidationError(
                self.error_messages['past_start'],
                code='past_start',
            )
        return start_date

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        start_date = self.cleaned_data.get('start_date')

        if start_date:
            if due_date < start_date:
                raise forms.ValidationError(
                    self.error_messages['due_before_start'],
                    code='due_before_start',
                )
        return due_date
