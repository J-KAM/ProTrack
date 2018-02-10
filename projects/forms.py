from django import forms

from . models import Project


class CreateProjectForm(forms.ModelForm):
    project_type = forms.ChoiceField(choices=[('p', 'ProTrack'), ('g', 'GitHub')], initial='p')
    owner_type = forms.ChoiceField(choices=[('m', 'Myself'), ('o', 'Organization')], initial='o')

    error_messages = {
        'git_owner_empty': 'You must enter a git repository owner username.',
        'git_name_empty': 'You must enter a git repository name.'
    }

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

    def clean_git_owner(self):
        project_type = self.cleaned_data.get('project_type')
        git_owner = self.cleaned_data.get('git_owner')
        if project_type == 'g' and git_owner == '':
            raise forms.ValidationError(
                self.error_messages['git_owner_empty'],
                code='git_owner_empty',
            )
        return git_owner

    def clean_git_name(self):
        project_type = self.cleaned_data.get('project_type')
        git_name = self.cleaned_data.get('git_name')
        if project_type == 'g' and git_name == '':
            raise forms.ValidationError(
                self.error_messages['git_name_empty'],
                code='git_name_empty',
            )
        return git_name


class UpdateProjectForm(forms.ModelForm):
    project_type = forms.ChoiceField(choices=[('p', 'ProTrack'), ('g', 'GitHub')])

    error_messages = {
        'git_owner_empty': 'You must enter a git repository owner username.',
        'git_name_empty': 'You must enter a git repository name.'
    }

    class Meta:
        model = Project
        fields = ['name', 'project_type', 'git_owner', 'git_name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none'}),
        }

    def clean_git_owner(self):
        project_type = self.cleaned_data.get('project_type')
        git_owner = self.cleaned_data.get('git_owner')
        if project_type == 'g' and git_owner == '':
            raise forms.ValidationError(
                self.error_messages['git_owner_empty'],
                code='git_owner_empty',
            )
        return git_owner

    def clean_git_name(self):
        project_type = self.cleaned_data.get('project_type')
        git_name = self.cleaned_data.get('git_name')
        if project_type == 'g' and git_name == '':
            raise forms.ValidationError(
                self.error_messages['git_name_empty'],
                code='git_name_empty',
            )
        return git_name