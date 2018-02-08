from django import forms

from . models import Project


class CreateProjectForm(forms.ModelForm):
    project_type = forms.ChoiceField(choices=[('p', 'ProTrack'), ('g', 'GitHub')], initial='p')
    owner_type = forms.ChoiceField(choices=[('m', 'Myself'), ('o', 'Organization')], initial='o')

    class Meta:
        model = Project
        fields = ['name', 'project_type', 'git_owner', 'git_name', 'owner_type', 'organization_owner', 'description']
        labels = {
            'owner_type': 'Owner',
            'organization_owner': 'Organization',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none'}),
        }


class UpdateProjectForm(forms.ModelForm):
    project_type = forms.ChoiceField(choices=[('p', 'ProTrack'), ('g', 'GitHub')])

    class Meta:
        model = Project
        fields = ['name', 'project_type', 'git_owner', 'git_name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none'}),
        }