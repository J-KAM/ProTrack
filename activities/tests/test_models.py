import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils.timezone import utc

from activities.models import Activity
from issues.models import Issue
from milestones.models import Milestone
from projects.models import Project


class ActivityModelTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',
                                              first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',description='my first project', created='2018-02-01', num_of_stars=0,owner=test_user1, organization_owner=None)

        self.PRO1_ID = test_project1.id

        milestone1 = Milestone.objects.create(name='Initial', description='my inital milestone',
                                              start_date='2018-02-03', due_date='2018-02-07', total_progress=0,
                                              total_time_spent=0.0, status='OPEN', project=test_project1)

        self.MILE1_ID = milestone1.id

        issue1 = Issue.objects.create(title="Issue 1", description="my issue 1", weight='3', progress='0%',
                                      type='Bug', status='Open', priority='Normal', project=test_project1,
                                      milestone=milestone1)
        self.ISS1_ID = issue1.id

        activity1 = Activity.objects.create(user=test_user1, action='opened', content_type=ContentType.objects.get_for_model(Issue), object_id=issue1.id,
                                            date_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        self.ACT1_ID = activity1.id

    def test_field_labels(self):
        activity = Activity.objects.get(id=self.ACT1_ID)

        user_label = activity._meta.get_field('user').verbose_name
        action_label = activity._meta.get_field('action').verbose_name
        content_type_label = activity._meta.get_field('content_type').verbose_name
        object_id_label = activity._meta.get_field('object_id').verbose_name
        date_time_label = activity._meta.get_field('date_time').verbose_name
        content_label = activity._meta.get_field('content').verbose_name
        content_id_label = activity._meta.get_field('content_id').verbose_name

        self.assertEqual(user_label, 'user')
        self.assertEqual(action_label, 'action')
        self.assertEqual(content_type_label, 'content type')
        self.assertEqual(object_id_label, 'object id')
        self.assertEqual(date_time_label, 'date time')
        self.assertEqual(content_label, 'content')
        self.assertEqual(content_id_label, 'content id')

    def test_field_nullable(self):
        activity = Activity.objects.get(id=self.ACT1_ID)

        user_nullable = activity._meta.get_field('user').null
        action_nullable = activity._meta.get_field('action').null
        content_type_nullable = activity._meta.get_field('content_type').null
        object_id_nullable = activity._meta.get_field('object_id').null
        date_time_nullable = activity._meta.get_field('date_time').null
        content_nullable = activity._meta.get_field('content').null
        content_id_nullable = activity._meta.get_field('content_id').null

        self.assertFalse(user_nullable)
        self.assertFalse(action_nullable)
        self.assertFalse(content_type_nullable)
        self.assertFalse(object_id_nullable)
        self.assertFalse(date_time_nullable)
        self.assertTrue(content_nullable)
        self.assertTrue(content_id_nullable)

    def test_field_lengths(self):
        activity = Activity.objects.get(id=self.ACT1_ID)
        action_length = activity._meta.get_field('action').max_length
        content_length = activity._meta.get_field('content').max_length

        self.assertEqual(action_length, 17)
        self.assertEqual(content_length, 255)

    def test_choices(self):
        activity = Activity.objects.get(id=self.ACT1_ID)
        choices = activity._meta.get_field('action').choices

        self.assertEqual(len(choices), 10)

    def test_object_name(self):
        activity = Activity.objects.get(id=self.ACT1_ID)
        user1 = User.objects.get(id=self.USER1_ID)
        self.assertEqual(user1.username + "-" + activity.action, str(activity))

    def test_content_object_values(self):
        activity = Activity.objects.get(id=self.ACT1_ID)
        issue1 = Issue.objects.get(id=self.ISS1_ID)

        self.assertEquals(activity.content_object, issue1)

        
        

