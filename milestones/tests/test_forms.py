from datetime import date

from django.test import TestCase

from django.contrib.auth.models import User

from milestones.forms import MilestoneForm
from projects.models import Organization, Project


class MilestoneFormTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create(username='pera', email='pera@gmail.com', password='pera1234',
                                         first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

        test_organization1 = Organization.objects.create(name='JKAM', owner=test_user1)
        self.ORG1_ID = test_organization1.id

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',
                                               description='my first project', created='2018-02-01', num_of_stars=0,
                                               owner=test_user1, organization_owner=None)
        test_project2 = Project.objects.create(name='MySecond', url='localhost:8000/JKAM/MySecond',
                                               description='my second project', created='2018-01-15', num_of_stars=0,
                                               owner=None, organization_owner=test_organization1)

        self.PRO1_ID = test_project1.id
        self.PRO2_ID = test_project2.id

    def test_field_labels(self):
        form = MilestoneForm()

        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')
        self.assertTrue(form.fields['project'].label is None or form.fields['project'].label == 'Project')
        self.assertTrue(form.fields['start_date'].label is None or form.fields['start_date'].label == 'Start date')
        self.assertTrue(form.fields['due_date'].label is None or form.fields['due_date'].label == 'Due date')
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Description')

    def test_required_fields(self):
        form = MilestoneForm()

        self.assertTrue(form.fields['name'].required)
        self.assertTrue(form.fields['project'].required)
        self.assertTrue(form.fields['start_date'].required)
        self.assertTrue(form.fields['due_date'].required)
        self.assertFalse(form.fields['description'].required)

    def test_date_widget(self):
        form = MilestoneForm()

        self.assertEqual(date.today, form.fields['start_date'].initial)
        self.assertEqual('%m/%d/%Y', form.fields['start_date'].widget.format)
        self.assertEqual(date.today, form.fields['due_date'].initial)
        self.assertEqual('%m/%d/%Y', form.fields['due_date'].widget.format)

    def test_field_number(self):
        form = MilestoneForm()

        self.assertEquals(len(form.fields), 5)

    def test_valid_form(self):
        project = Project.objects.get(id=self.PRO1_ID)

        form_data = {
            'name': 'My first milestone',
            'project': str(project.id),
            'start_date': '2018-02-10',
            'due_date': '2018-02-15',
            'description': 'milestone description'
        }

        form = MilestoneForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_past_start_invalid_form(self):
        project = Project.objects.get(id=self.PRO1_ID)

        form_data = {
            'name': 'My first milestone',
            'project': str(project.id),
            'start_date': '2018-01-01',
            'due_date': '2018-02-15',
            'description': 'milestone description'
        }

        form = MilestoneForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_due_before_start_invalid_form(self):
        project = Project.objects.get(id=self.PRO1_ID)

        form_data = {
            'name': 'My first milestone',
            'project': str(project.id),
            'start_date': '2018-03-10',
            'due_date': '2018-03-01',
            'description': 'milestone description'
        }

        form = MilestoneForm(data=form_data)
        self.assertFalse(form.is_valid())