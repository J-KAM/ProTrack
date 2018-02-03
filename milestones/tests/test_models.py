from django.contrib.auth.models import User
from django.test import TestCase

from milestones.models import Milestone
from organizations.models import Organization
from projects.models import Project


#Date of running these tests: 03.02.2018

class MilestoneModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera',last_name='Peric')
        test_organization1 = Organization.objects.create(name='JKAM', owner=test_user1)

        test_user1.save()
        test_organization1.save()

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',description='my first project', created='2018-02-01', num_of_stars=0,owner=test_user1, organization_owner=None)
        test_project2 = Project.objects.create(name='MySecond', url='localhost:8000/JKAM/MySecond', description='my second project', created='2018-01-15', num_of_stars=0,owner=None, organization_owner=test_organization1)

        test_project1.save()
        test_project2.save()

        milestone1 = Milestone.objects.create(name='Initial', description = 'my inital milestone', start_date = '2018-02-03', due_date = '2018-02-07', total_progress=0, total_time_spent=0.0, status = 'OPEN', project=test_project1)
        milestone2 = Milestone.objects.create(name='User management', description='um milestone',
                                              start_date='2018-01-03', due_date='2018-01-15', total_progress=100,
                                              total_time_spent=4.5, status='CLOSED', project=test_project1)
        milestone3 = Milestone.objects.create(name='Testing', description='testing milestone',
                                              start_date='2018-02-01', due_date='2018-02-02', total_progress=60,
                                              total_time_spent=2.0, status='OPEN', project=test_project2)
        milestone1.save()
        milestone2.save()
        milestone3.save()

    def test_field_labels(self):
        milestone = Milestone.objects.get(id=1)
        name_label = milestone._meta.get_field('name').verbose_name
        description_label = milestone._meta.get_field('description').verbose_name
        start_date_label = milestone._meta.get_field('start_date').verbose_name
        due_date_label = milestone._meta.get_field('due_date').verbose_name
        total_progress_label = milestone._meta.get_field('total_progress').verbose_name
        total_time_spent_label = milestone._meta.get_field('total_time_spent').verbose_name
        status_label = milestone._meta.get_field('status').verbose_name
        project_label = milestone._meta.get_field('project').verbose_name

        self.assertEqual(name_label, 'name')
        self.assertEqual(description_label, 'description')
        self.assertEqual(start_date_label, 'start date')
        self.assertEqual(due_date_label, 'due date')
        self.assertEqual(total_progress_label, 'total progress')
        self.assertEqual(total_time_spent_label, 'total time spent')
        self.assertEqual(status_label, 'status')
        self.assertEqual(project_label, 'project')

    def test_field_nullable(self):
        milestone = Milestone.objects.get(id=1)
        name_nullable = milestone._meta.get_field('name').null
        description_nullable = milestone._meta.get_field('description').null
        start_date_nullable = milestone._meta.get_field('start_date').null
        due_date_nullable = milestone._meta.get_field('due_date').null
        total_progress_nullable = milestone._meta.get_field('total_progress').null
        total_time_spent_nullable = milestone._meta.get_field('total_time_spent').null
        status_nullable = milestone._meta.get_field('status').null
        project_nullable = milestone._meta.get_field('project').null

        self.assertFalse(name_nullable)
        self.assertTrue(description_nullable)
        self.assertFalse(start_date_nullable)
        self.assertFalse(due_date_nullable)
        self.assertFalse(total_progress_nullable)
        self.assertFalse(total_time_spent_nullable)
        self.assertFalse(status_nullable)
        self.assertFalse(project_nullable)

    def test_default_values(self):
        milestone = Milestone.objects.get(id=1)
        total_progress_default = milestone._meta.get_field('total_progress').default
        total_time_spent_default = milestone._meta.get_field('total_time_spent').default
        status_default = milestone._meta.get_field('status').default

        self.assertEqual(total_progress_default, 0)
        self.assertEqual(total_time_spent_default, 0.0)
        self.assertEqual(status_default, "OPEN")

    def test_field_lengths(self):
        milestone = Milestone.objects.get(id=1)
        name_length = milestone._meta.get_field('name').max_length
        status_length = milestone._meta.get_field('status').max_length

        self.assertEqual(name_length, 80)
        self.assertEqual(status_length, 6)

    def test_choices(self):
        milestone = Milestone.objects.get(id=1)
        choices = milestone._meta.get_field('status').choices

        self.assertEqual(len(choices), 2)

    def test_object_name(self):
        milestone = Milestone.objects.get(id=1)
        self.assertEqual('Initial', str(milestone))

    def test_is_past_due(self):
        milestone1 = Milestone.objects.get(id=1)
        milestone2 = Milestone.objects.get(id=2)
        milestone3 = Milestone.objects.get(id=3)

        self.assertFalse(milestone1.is_past_due)
        self.assertFalse(milestone2.is_past_due)
        self.assertTrue(milestone3.is_past_due)

    def test_name_values(self):
        milestone1 = Milestone.objects.get(id=1)
        milestone2 = Milestone.objects.get(id=2)
        milestone3 = Milestone.objects.get(id=3)

        self.assertEquals(milestone1.name, 'Initial')
        self.assertEquals(milestone2.name, 'User management')
        self.assertEquals(milestone3.name, 'Testing')

    def test_project_values(self):
        project1 = Project.objects.get(id=1)
        project2 = Project.objects.get(id=2)

        milestone1 = Milestone.objects.get(id=1)
        milestone2 = Milestone.objects.get(id=2)
        milestone3 = Milestone.objects.get(id=3)

        self.assertEquals(milestone1.project, project1)
        self.assertEquals(milestone2.project, project1)
        self.assertEquals(milestone3.project, project2)



