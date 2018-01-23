from django import forms

from issues.models import Issue
from issues.models import WEIGHT_CHOICES, TYPE_CHOICES, STATUS_CHOICES, PROGRESS_CHOICES, PRIORITY_CHOICES


class IssueForm(forms.ModelForm):
    weight = forms.ChoiceField(required=False, choices=WEIGHT_CHOICES)
    progress = forms.ChoiceField(required=False, choices=PROGRESS_CHOICES)
    time_spent = forms.FloatField(required=False, initial=0, min_value=0.0)
    type = forms.ChoiceField(required=False, choices=TYPE_CHOICES)
    status = forms.ChoiceField(required=False, choices=STATUS_CHOICES)
    priority = forms.ChoiceField(required=False, choices=PRIORITY_CHOICES)

    class Meta:
        model = Issue
        fields = ['title', 'description', 'time_spent', 'progress', 'type', 'weight', 'priority', 'status']
        widgets = {'description': forms.Textarea(attrs={'rows': 6, 'cols': 43,
                                                        'style': 'resize:none;'}),
        }
