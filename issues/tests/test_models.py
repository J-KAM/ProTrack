from django.contrib.auth.models import User
from django.test import TestCase

from issues.models import Issue
from milestones.models import Milestone
from projects.models import Project


class IssueModelTest(TestCase):

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
        issue = Issue.objects.get(id=self.ISS1_ID)
        title_label = issue._meta.get_field('title').verbose_name
        description_label = issue._meta.get_field('description').verbose_name
        weight_label = issue._meta.get_field('weight').verbose_name
        progress_label = issue._meta.get_field('progress').verbose_name
        time_spent_label = issue._meta.get_field('time_spent').verbose_name
        type_label = issue._meta.get_field('type').verbose_name
        status_label = issue._meta.get_field('status').verbose_name
        priority_label = issue._meta.get_field('priority').verbose_name
        total_time_spent_label = issue._meta.get_field('total_time_spent').verbose_name
        project_label = issue._meta.get_field('project').verbose_name
        milestone_label = issue._meta.get_field('milestone').verbose_name

        self.assertEqual(title_label, 'title')
        self.assertEqual(description_label, 'description')
        self.assertEqual(weight_label, 'weight')
        self.assertEqual(progress_label, 'progress')
        self.assertEqual(time_spent_label, 'time spent')
        self.assertEqual(type_label, 'type')
        self.assertEqual(status_label, 'status')
        self.assertEqual(priority_label, 'priority')
        self.assertEqual(total_time_spent_label, 'total time spent')
        self.assertEqual(project_label, 'project')
        self.assertEqual(milestone_label, 'milestone')

    def test_field_nullable(self):
        issue = Issue.objects.get(id=self.ISS1_ID)
        title_nullable = issue._meta.get_field('title').null
        description_nullable = issue._meta.get_field('description').null
        weight_nullable = issue._meta.get_field('weight').null
        progress_nullable = issue._meta.get_field('progress').null
        time_spent_nullable = issue._meta.get_field('time_spent').null
        type_nullable = issue._meta.get_field('type').null
        status_nullable = issue._meta.get_field('status').null
        priority_nullable = issue._meta.get_field('priority').null
        total_time_spent_nullable = issue._meta.get_field('total_time_spent').null
        project_nullable = issue._meta.get_field('project').null
        milestone_nullable = issue._meta.get_field('milestone').null

        self.assertFalse(title_nullable)
        self.assertTrue(description_nullable)
        self.assertTrue(weight_nullable)
        self.assertTrue(progress_nullable)
        self.assertFalse(time_spent_nullable)
        self.assertTrue(type_nullable)
        self.assertTrue(status_nullable)
        self.assertTrue(priority_nullable)
        self.assertFalse(total_time_spent_nullable)
        self.assertFalse(project_nullable)
        self.assertTrue(milestone_nullable)

    def test_default_values(self):
        issue = Issue.objects.get(id=self.ISS1_ID)
        time_spent_default = issue._meta.get_field('time_spent').default
        total_time_spent_default = issue._meta.get_field('total_time_spent').default

        self.assertEqual(time_spent_default, 0.0)
        self.assertEqual(total_time_spent_default, 0.0)

    def test_field_lengths(self):
        issue = Issue.objects.get(id=self.ISS1_ID)
        title_length = issue._meta.get_field('title').max_length
        progress_length = issue._meta.get_field('progress').max_length
        type_length = issue._meta.get_field('type').max_length
        status_length = issue._meta.get_field('status').max_length
        priority_length = issue._meta.get_field('priority').max_length

        self.assertEqual(title_length, 80)
        self.assertEqual(progress_length, 4)
        self.assertEqual(type_length, 30)
        self.assertEqual(status_length, 20)
        self.assertEqual(priority_length, 10)

    def test_choices(self):
        issue = Issue.objects.get(id=self.ISS1_ID)
        weight_choices = issue._meta.get_field('weight').choices
        progress_choices = issue._meta.get_field('progress').choices
        type_choices = issue._meta.get_field('type').choices
        status_choices = issue._meta.get_field('status').choices
        priority_choices = issue._meta.get_field('priority').choices

        self.assertEqual(len(weight_choices), 5)
        self.assertEqual(len(progress_choices), 11)
        self.assertEqual(len(type_choices), 5)
        self.assertEqual(len(status_choices), 4)
        self.assertEqual(len(priority_choices), 4)

    def test_object_name(self):
        issue = Issue.objects.get(id=self.ISS1_ID)
        self.assertEqual('Issue 1', str(issue))

    def test_progress_in_numbers(self):
        issue = Issue.objects.get(id=self.ISS1_ID)
        self.assertEqual(issue.progress_in_numbers(), '0')

    def test_name_values(self):
        issue1 = Issue.objects.get(id=self.ISS1_ID)
        issue2 = Issue.objects.get(id=self.ISS2_ID)
        issue3 = Issue.objects.get(id=self.ISS3_ID)

        self.assertEquals(issue1.title, 'Issue 1')
        self.assertEquals(issue2.title, 'Issue 2')
        self.assertEquals(issue3.title, 'Issue 3')

    def test_project_values(self):
        project1 = Project.objects.get(id=self.PRO1_ID)
        project2 = Project.objects.get(id=self.PRO2_ID)

        issue1 = Issue.objects.get(id=self.ISS1_ID)
        issue2 = Issue.objects.get(id=self.ISS2_ID)
        issue3 = Issue.objects.get(id=self.ISS3_ID)

        self.assertEquals(issue1.project, project1)
        self.assertEquals(issue2.project, project2)
        self.assertEquals(issue3.project, project1)

    def test_milestone_values(self):
        milestone1 = Milestone.objects.get(id=self.MILE1_ID)

        issue1 = Issue.objects.get(id=self.ISS1_ID)
        issue2 = Issue.objects.get(id=self.ISS2_ID)
        issue3 = Issue.objects.get(id=self.ISS3_ID)

        self.assertEquals(issue1.milestone, milestone1)
        self.assertEquals(issue2.milestone, milestone1)
        self.assertEquals(issue3.milestone, None)









