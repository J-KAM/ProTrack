from django.test import TestCase

from projects.forms import CreateProjectForm, UpdateProjectForm


class CreateProjectFormTest(TestCase):

    def test_field_labels(self):
        form = CreateProjectForm()

        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')
        self.assertTrue(form.fields['project_type'].label is None or form.fields['project_type'].label == 'Project type')
        self.assertTrue(form.fields['git_owner'].label is None or form.fields['git_owner'].label == 'Git owner')
        self.assertTrue(form.fields['git_name'].label is None or form.fields['git_name'].label == 'Git name')
        self.assertTrue(form.fields['owner_type'].label is None or form.fields['owner_type'].label == 'Owner')
        self.assertTrue(form.fields['organization_owner'].label is None or form.fields['organization_owner'].label == 'Organization')
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Description')

    def test_required_fields(self):
        form = CreateProjectForm()

        self.assertTrue(form.fields['name'].required)
        self.assertTrue(form.fields['project_type'].required)
        self.assertFalse(form.fields['git_owner'].required)
        self.assertFalse(form.fields['git_name'].required)
        self.assertTrue(form.fields['owner_type'].required)
        self.assertTrue(form.fields['organization_owner'].required)
        self.assertFalse(form.fields['description'].required)

    def test__initial_values(self):
        form = CreateProjectForm()

        self.assertEqual(form.fields['project_type'].initial, 'p')
        self.assertEqual(form.fields['owner_type'].initial, 'o')

    def test_field_number(self):
        form = CreateProjectForm()

        self.assertEqual(len(form.fields), 7)

    def test_invalid_form(self):
        form_data = {
            'name': 'Project',
            'description': 'opis projekta'
        }

        form = CreateProjectForm(data=form_data)
        self.assertFalse(form.is_valid())


class UpdateProjectFormTest(TestCase):

    def test_field_labels(self):
        form = UpdateProjectForm()

        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')
        self.assertTrue(form.fields['project_type'].label is None or form.fields['project_type'].label == 'Project type')
        self.assertTrue(form.fields['git_owner'].label is None or form.fields['git_owner'].label == 'Git owner')
        self.assertTrue(form.fields['git_name'].label is None or form.fields['git_name'].label == 'Git name')
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Description')

    def test_required_fields(self):
        form = UpdateProjectForm()

        self.assertTrue(form.fields['name'].required)
        self.assertTrue(form.fields['project_type'].required)
        self.assertFalse(form.fields['git_owner'].required)
        self.assertFalse(form.fields['git_name'].required)
        self.assertFalse(form.fields['description'].required)

    def test_field_number(self):
        form = UpdateProjectForm()

        self.assertEqual(len(form.fields), 5)

    def test_valid_form(self):
        form_data = {
            'name': 'Project',
            'project_type': 'g',
            'git_owner': 'J-KAM',
            'git_name': 'ProPRo',
            'description': 'opis projekta'
        }

        form = UpdateProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'description': 'opis projekta'
        }

        form = UpdateProjectForm(data=form_data)
        self.assertFalse(form.is_valid())