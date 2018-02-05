from django import forms

from . models import Project


class CreateProjectForm(forms.ModelForm):
    owner_type = forms.ChoiceField(choices=[('m', 'Myself'), ('o', 'Organization')], initial='o')

    class Meta:
        model = Project
        fields = ['name', 'owner_type', 'organization_owner', 'description']
        labels = {
            'organization_owner': 'Organization',
            'owner_type': 'Owner',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none'}),
        }


class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none'}),
        }