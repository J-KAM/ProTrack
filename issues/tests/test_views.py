from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from issues.models import Issue
from milestones.models import Milestone
from projects.models import Project


class IssueFormViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id
        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',
                                               description='my first project', created='2018-02-01', num_of_stars=0,
                                               owner=test_user1, organization_owner=None)

        self.PRO1_ID = test_project1.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('issues:create', kwargs={'project_id': self.PRO1_ID}))
        self.assertRedirects(response, '/?next=/issues/' + str(self.PRO1_ID) + '/new/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get(reverse('issues:create', kwargs={'project_id': self.PRO1_ID}))

        self.assertEqual(str(response.context['user']), 'pera')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issues/issue_form.html')

    def test_issue_creating(self):
        issue_data = {
            'title': 'My first issue',
            'description': 'My first issue description',
            'time_spent': 0,
            'progress': '0%',
            'type': 'Feature',
            'priority': 'Normal',
            'assignees': [str(self.USER1_ID)],
            'status': 'Open',
            'weight': 1,

        }

        login = self.client.login(username='pera', password='pera1234')
        response = self.client.post(reverse('issues:create', kwargs={'project_id': self.PRO1_ID}), issue_data)
        self.assertEqual(response.status_code, 302)


class IssuePreviewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

    # def test_urls_exist_at_desired_location(self):
    #     login = self.client.login(username='pera', password='pera1234')
    #     response = self.client.get('/issues/all/')
    #
    #     self.assertEqual(str(response.context['user']), 'pera')
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.get('/issues/assigned/')
    #
    #     self.assertEqual(str(response.context['user']), 'pera')
    #     self.assertEqual(response.status_code, 200)
    #
    #
    # def test_view_accessible_by_urls(self):
    #     login = self.client.login(username='pera', password='pera1234')
    #
    #     response = self.client.get(reverse('issues:preview_all'))
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.get(reverse('issues:preview_assigned'))
    #     self.assertEqual(response.status_code, 200)

    # def test_logged_in_uses_correct_template(self):
    #     login = self.client.login(username='pera', password='pera1234')
    #     response = self.client.get(reverse('issues:preview_all'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'issues/preview.html')
    #
    #     response = self.client.get(reverse('issues:preview_assigned'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'issues/preview.html')


class IssueDetailTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',
                                               description='my first project', created='2018-02-01', num_of_stars=0,
                                               owner=test_user1, organization_owner=None)

        self.PRO1_ID = test_project1.id

        issue1 = Issue.objects.create(title="Issue 1", description="my issue 1", weight='3', progress='0%',
                                      type='Bug', status='Open', priority='Normal', project=test_project1,
                                      )
        self.ISS1_ID = issue1.id

    def test_urls_exist_at_desired_location(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get('/issues/' + str(self.ISS1_ID) + '/details/')

        self.assertEqual(str(response.context['user']), 'pera')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_urls(self):
        login = self.client.login(username='pera', password='pera1234')

        response = self.client.get(reverse('issues:details', kwargs={'id': self.ISS1_ID}))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get(reverse('issues:details', kwargs={'id': self.ISS1_ID}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issues/issue_details.html')


class IssueUpdateViewTest(TestCase):

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

        issue1 = Issue.objects.create(title="Issue 1", description="my issue 1", weight='3', progress='0%',
                                      type='Bug', status='Open', priority='Normal', project=test_project1,
                                      )
        issue2 = Issue.objects.create(title="Issue 2", description="my issue 2", weight='3', progress='0%',
                                      type='Bug', status='Open', priority='Normal', project=test_project1, milestone=milestone1
                                      )
        self.ISS1_ID = issue1.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('issues:update', kwargs={'id': self.ISS1_ID}))
        self.assertRedirects(response, '/?next=/issues/' + str(self.ISS1_ID) + '/')

    def test_logged_in(self):
        login = self.client.login(username="pera", password="pera1234")
        response = self.client.get(reverse('issues:update', kwargs={'id': self.ISS1_ID}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issues/issue_form.html')

    def test_issue_update(self):
        login = self.client.login(username="pera", password="pera1234")

        issue_data = {
            'title': 'Issue1',
            'description': 'My first issue description',
            'time_spent': 0,
            'progress': '0%',
            'type': 'Feature',
            'priority': 'Normal',
            'assignees': [str(self.USER1_ID)],
            'status': 'Open',
            'weight': 1,

        }

        response = self.client.post(reverse('issues:update', kwargs={'id': self.ISS1_ID}), issue_data)
        self.assertEqual(response.status_code, 302)

        issue = Issue.objects.get(id=self.ISS1_ID)
        self.assertEqual(issue.description, 'My first issue description')

    def test_milestone_update(self):
        login = self.client.login(username="pera", password="pera1234")

        issue_data = {
            'title': 'Issue1',
            'description': 'My first issue description',
            'time_spent': 2,
            'milestone': str(self.MILE1_ID),
            'progress': '40%',
            'type': 'Feature',
            'priority': 'Normal',
            'assignees': [str(self.USER1_ID)],
            'status': 'Open',
            'weight': 1,

        }

        response = self.client.post(reverse('issues:update', kwargs={'id': self.ISS1_ID}), issue_data)
        self.assertEqual(response.status_code, 302)

        milestone = Milestone.objects.get(id=self.MILE1_ID)
        self.assertEqual(milestone.total_time_spent, 2.0)

class ViewMethodsTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',
                                              first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',
                                               description='my first project', created='2018-02-01', num_of_stars=0,
                                               owner=test_user1, organization_owner=None)

        self.PRO1_ID = test_project1.id

        issue1 = Issue.objects.create(title="Issue 1", description="my issue 1", weight='3', progress='0%',
                                      type='Bug', status='Open', priority='Normal', project=test_project1,
                                      )
        self.ISS1_ID = issue1.id

    def test_redirect_if_not_logged_in_close_and_reopen(self):
        response = self.client.get(reverse('issues:close', kwargs={'id': self.ISS1_ID}))
        self.assertRedirects(response, '/?next=/issues/' + str(self.ISS1_ID) + '/close/')

        response = self.client.get(reverse('issues:reopen', kwargs={'id': self.ISS1_ID}))
        self.assertRedirects(response, '/?next=/issues/' + str(self.ISS1_ID) + '/reopen/')

    def test_logged_in_close_and_reopen(self):
        login = self.client.login(username="pera", password="pera1234")
        response = self.client.get(reverse('issues:close', kwargs={'id': self.ISS1_ID}))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('issues:reopen', kwargs={'id': self.ISS1_ID}))
        self.assertEqual(response.status_code, 302)





