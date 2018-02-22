
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from comments.models import Comment
from issues.models import Issue
from milestones.models import Milestone
from projects.models import Project


class CommentModelTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',
                                              first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',
                                               description='my first project', created='2018-02-01', num_of_stars=0,
                                               owner=test_user1, organization_owner=None)

        self.PRO1_ID = test_project1.id

        milestone1 = Milestone.objects.create(name='Initial', description='my inital milestone',
                                              start_date='2018-02-03', due_date='2018-02-07', total_progress=0,
                                              total_time_spent=0.0, status='OPEN', project=test_project1)

        self.MILE1_ID = milestone1.id

        issue1 = Issue.objects.create(title="Issue 1", description="my issue 1", weight='3', progress='0%',
                                      type='Bug', status='Open', priority='Normal', project=test_project1,
                                      milestone=milestone1)
        self.ISS1_ID = issue1.id

        comment1 = Comment.objects.create(user=test_user1, text='my first milestone comment',
                                            content_type=ContentType.objects.get_for_model(Milestone),
                                            object_id=milestone1.id)
        self.COM1_ID = comment1.id

        comment2 = Comment.objects.create(user=test_user1, text='my second milestone comment',
                                            content_type=ContentType.objects.get_for_model(Milestone),
                                            object_id=milestone1.id)
        self.COM2_ID = comment2.id

        comment3 = Comment.objects.create(user=test_user1, text='my first issue comment',
                                          content_type=ContentType.objects.get_for_model(Issue),
                                          object_id=issue1.id)
        self.COM3_ID = comment3.id

    def test_field_labels(self):
        comment = Comment.objects.get(id=self.COM1_ID)

        user_label = comment._meta.get_field('user').verbose_name
        date_time_label = comment._meta.get_field('date_time').verbose_name
        text_label = comment._meta.get_field('text').verbose_name
        content_type_label = comment._meta.get_field('content_type').verbose_name
        object_id_label = comment._meta.get_field('object_id').verbose_name
        comments_label = comment._meta.get_field('comments').verbose_name

        self.assertEqual(user_label, 'user')
        self.assertEqual(date_time_label, 'date time')
        self.assertEqual(text_label, 'text')
        self.assertEqual(content_type_label, 'content type')
        self.assertEqual(object_id_label, 'object id')
        self.assertEqual(comments_label, 'comments')

    def test_field_nullable(self):
        comment = Comment.objects.get(id=self.COM1_ID)

        user_nullable = comment._meta.get_field('user').null
        date_time_nullable = comment._meta.get_field('date_time').null
        text_nullable = comment._meta.get_field('text').null
        content_type_nullable = comment._meta.get_field('content_type').null
        object_id_nullable = comment._meta.get_field('object_id').null
        comments_nullable = comment._meta.get_field('comments').null

        self.assertFalse(user_nullable)
        self.assertFalse(date_time_nullable)
        self.assertFalse(text_nullable)
        self.assertFalse(content_type_nullable)
        self.assertFalse(object_id_nullable)
        self.assertFalse(comments_nullable)

    def test_object_name(self):
        comment = Comment.objects.get(id=self.COM1_ID)
        self.assertEqual('my first milestone comment', str(comment))

    def test_content_object_values(self):
        comment1_milestone = Comment.objects.get(id=self.COM1_ID)
        comment2_milestone = Comment.objects.get(id=self.COM2_ID)
        milestone = Milestone.objects.get(id=self.MILE1_ID)
        comment3_issue = Comment.objects.get(id=self.COM3_ID)
        issue = Issue.objects.get(id=self.ISS1_ID)

        self.assertEquals(comment1_milestone.content_object, milestone)
        self.assertEquals(comment2_milestone.content_object, milestone)
        self.assertEquals(comment3_issue.content_object, issue)