from django.contrib.auth.models import User
from django.test import TestCase

from issues.forms import IssueForm
from issues.models import Issue
from milestones.models import Milestone
from projects.models import Project


class IssueFormTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',
                                              first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',description='my first project', created='2018-02-01', num_of_stars=0,owner=test_user1, organization_owner=None)
        test_project2 = Project.objects.create(name='Second project', url='localhost:8000/pera/Second project',description='my second project', created='2018-02-01', num_of_stars=0,owner=test_user1, organization_owner=None)

        self.PRO1_ID = test_project1.id
        self.PRO2_ID = test_project2.id

        milestone1 = Milestone.objects.create(name='Initial', description = 'my inital milestone', start_date = '2018-02-03', due_date = '2018-02-07', total_progress=0, total_time_spent=0.0, status = 'OPEN', project=test_project1)

        self.MILE1_ID = milestone1.id

        issue1 = Issue.objects.create(title="Issue 1", description="my issue 1", weight='3', progress='0%',
                                      type='Bug', status='Open', priority='Normal', project=test_project1, milestone=milestone1)
        self.ISS1_ID = issue1.id

        issue2 = Issue.objects.create(title="Issue 2", description="my issue 2", weight='3', progress='0%',
                                      type='Bug', status='Open', priority='Normal', project=test_project2,
                                      milestone=milestone1)
        self.ISS2_ID = issue2.id

        issue3 = Issue.objects.create(title="Issue 3", description="my issue 3", weight='3', progress='0%',
                                      type='Bug', status='Open', priority='Normal', project=test_project1,)
        self.ISS3_ID = issue3.id

    def test_field_labels(self):
        form = IssueForm()

        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'Title')
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Description')
        self.assertTrue(form.fields['weight'].label is None or form.fields['weight'].label == 'Weight')
        self.assertTrue(form.fields['progress'].label is None or form.fields['progress'].label == 'Progress')
        self.assertTrue(form.fields['time_spent'].label is None or form.fields['time_spent'].label == 'Time spent')
        self.assertTrue(form.fields['type'].label is None or form.fields['type'].label == 'Type')
        self.assertTrue(form.fields['status'].label is None or form.fields['status'].label == 'Status')
        self.assertTrue(form.fields['priority'].label is None or form.fields['priority'].label == 'Priority')
        self.assertTrue(form.fields['milestone'].label is None or form.fields['milestone'].label == 'Milestone')
        self.assertTrue(form.fields['assignees'].label is None or form.fields['assignees'].label == 'Assignees')

    def test_required_fields(self):
        form = IssueForm()

        self.assertTrue(form.fields['title'].required)
        self.assertFalse(form.fields['description'].required)
        self.assertFalse(form.fields['weight'].required)
        self.assertFalse(form.fields['progress'].required)
        self.assertFalse(form.fields['time_spent'].required)
        self.assertFalse(form.fields['type'].required)
        self.assertFalse(form.fields['status'].required)
        self.assertFalse(form.fields['priority'].required)

    def test_field_number(self):
        form = IssueForm()

        self.assertEquals(len(form.fields), 10)

    def test_invalid_form(self):
        milestone1 = Milestone.objects.get(id=self.MILE1_ID)
        user1 = User.objects.get(id=self.USER1_ID)

        form_data = {
            # title is required
            'description': 'My first issue description',
            'time_spent': '0.0',
            'progress': '0%',
            'milestone': str(milestone1.id),
            'type': 'Feature',
            'priority': 'Normal',
            'assignees': str(user1.id),
            'status': 'Open',

        }

        form = IssueForm(data=form_data)
        self.assertFalse(form.is_valid())
