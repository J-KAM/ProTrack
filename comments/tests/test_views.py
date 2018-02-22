from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from comments.models import Comment
from issues.models import Issue
from milestones.models import Milestone
from projects.models import Project


class CommentCreateTest(TestCase):

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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('comments:comment'))
        self.assertRedirects(response, '/?next=/comments/comment/')

    def test_issue_commenting(self):
        comment_data = {
            'resource_type': 'issue',
            'resource_id': str(self.ISS1_ID),
            'text': 'My first issue comment',
        }
        redirect_url = reverse('issues:details', kwargs={'id': self.ISS1_ID})
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.post(reverse('comments:comment'), comment_data, HTTP_REFERER=redirect_url)
        self.assertEqual(response.status_code, 302)

    def test_milestone_commenting(self):
        comment_data = {
            'resource_type': 'milestone',
            'resource_id': str(self.MILE1_ID),
            'text': 'My test comment',
        }
        redirect_url = reverse('milestones:detail', kwargs={'id': self.MILE1_ID})
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.post(reverse('comments:comment'), comment_data, HTTP_REFERER=redirect_url)
        self.assertEqual(response.status_code, 302)

    def test_comment_commenting(self):
        comment_data = {
            'resource_type': 'comment',
            'resource_id': str(self.COM1_ID),
            'text': 'My test reply',
        }
        redirect_url = reverse('milestones:detail', kwargs={'id': self.MILE1_ID})
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.post(reverse('comments:comment'), comment_data, HTTP_REFERER=redirect_url)
        self.assertEqual(response.status_code, 302)


class CommentUpdateTest(TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('comments:update'))
        self.assertRedirects(response, '/?next=/comments/update/')


class CommentDeleteTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',
                                               description='my first project', created='2018-02-01', num_of_stars=0,
                                               owner=test_user1, organization_owner=None)

        self.PRO1_ID = test_project1.id

        milestone1 = Milestone.objects.create(name='Initial', description='my inital milestone',
                                              start_date='2018-02-03', due_date='2018-02-07', total_progress=0,
                                              total_time_spent=0.0, status='OPEN', project=test_project1)
        self.MILE1_ID = milestone1.id

        comment1 = Comment.objects.create(user=test_user1, text='my first milestone comment',
                                          content_type=ContentType.objects.get_for_model(Milestone),
                                          object_id=milestone1.id)
        self.COM1_ID = comment1.id


    def test_view_accessible_by_urls(self):
        login = self.client.login(username='pera', password='pera1234')
        redirect_url = reverse('milestones:detail', kwargs={'id': self.MILE1_ID})
        response = self.client.get(reverse('comments:delete', kwargs={'comment_id': self.COM1_ID}), HTTP_REFERER=redirect_url)
        self.assertEqual(response.status_code, 302)