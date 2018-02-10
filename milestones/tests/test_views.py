from django.contrib.auth.models import User
from django.test import TestCase

from django.urls import reverse

from milestones.models import Milestone
from projects.models import Project


class MilestoneCreateViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id
        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',
                                               description='my first project', created='2018-02-01', num_of_stars=0,
                                               owner=test_user1, organization_owner=None)

        self.PRO1_ID = test_project1.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('milestones:create'))
        self.assertRedirects(response, '/?next=/milestones/new/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get(reverse('milestones:create'))

        self.assertEqual(str(response.context['user']), 'pera')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'milestones/milestone_form.html')

    def test_milestone_creating(self):
        milestone_data = {
            'name': 'New milestone',
            'project': str(self.PRO1_ID),
            'start_date': '2018-03-01',
            'due_date': '2018-03-15',
            'description': 'this is my description'
        }

        login = self.client.login(username='pera', password='pera1234')
        response = self.client.post(reverse('milestones:create'), milestone_data)
        self.assertEqual(response.status_code, 302)


class MilestoneUpdateViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',
                                               description='my first project', created='2018-02-01', num_of_stars=0,
                                               owner=test_user1, organization_owner=None)

        self.PRO1_ID = test_project1.id

        milestone1 = Milestone.objects.create(name='Initial', description='my inital milestone',
                                              start_date='2018-03-20', due_date='2018-03-25', total_progress=0,
                                              total_time_spent=0.0, status='OPEN', project=test_project1)
        self.MILE1_ID = milestone1.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('milestones:update', kwargs={'id': self.MILE1_ID}))
        self.assertRedirects(response, '/?next=/milestones/' + str(self.MILE1_ID) + '/')

    def test_logged_in(self):
        login = self.client.login(username="pera", password="pera1234")
        response = self.client.get(reverse('milestones:update', kwargs={'id': self.MILE1_ID}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'milestones/milestone_form.html')

    def test_milestone_update(self):
        login = self.client.login(username="pera", password="pera1234")

        milestone_data = {
            'name': 'Initial',
            'due_date': '2018-03-25',
            'description': 'New description'
        }

        response = self.client.post(reverse('milestones:update', kwargs={'id': self.MILE1_ID}), milestone_data)
        self.assertEqual(response.status_code, 302)

        milestone = Milestone.objects.get(id=self.MILE1_ID)
        self.assertEqual(milestone.description, 'New description')


class MilestonePreviewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

    # def test_url_exists_at_desired_location(self):
    #     login = self.client.login(username='pera', password='pera1234')
    #     response = self.client.get('/milestones/')
    #
    #     self.assertEqual(str(response.context['user']), 'pera')
    #     self.assertEqual(response.status_code, 200)

    # def test_view_accessible_by_url(self):
    #     login = self.client.login(username='pera', password='pera1234')
    #
    #     response = self.client.get(reverse('milestones:preview'))
    #     self.assertEqual(response.status_code, 200)

    # def test_logged_in_uses_correct_template(self):
    #     login = self.client.login(username='pera', password='pera1234')
    #     response = self.client.get(reverse('milestones:preview'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'milestones/preview.html')


class MilestoneDeleteTest(TestCase):

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

    def test_urls_exist_at_desired_location(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get('/milestones/' + str(self.MILE1_ID) + '/delete/')

        self.assertEqual(str(response.context['user']), 'pera')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_urls(self):
        login = self.client.login(username='pera', password='pera1234')

        response = self.client.get(reverse('milestones:delete', kwargs={'pk': self.MILE1_ID}))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get(reverse('milestones:delete', kwargs={'pk': self.MILE1_ID}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'milestones/milestone_confirm_delete.html')


class MilestoneDetailTest(TestCase):
    def test_urls_exist_at_desired_location(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get('/milestones/' + str(self.MILE1_ID) + '/details/')

        self.assertEqual(str(response.context['user']), 'pera')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_urls(self):
        login = self.client.login(username='pera', password='pera1234')

        response = self.client.get(reverse('milestones:detail', kwargs={'id': self.MILE1_ID}))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get(reverse('milestones:detail', kwargs={'id': self.MILE1_ID}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'milestones/detail_preview.html')

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

    def test_urls_exist_at_desired_location(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get('/milestones/' + str(self.MILE1_ID) + '/details/')

        self.assertEqual(str(response.context['user']), 'pera')
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_urls(self):
        login = self.client.login(username='pera', password='pera1234')

        response = self.client.get(reverse('milestones:detail', kwargs={'id': self.MILE1_ID}))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get(reverse('milestones:detail', kwargs={'id': self.MILE1_ID}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'milestones/detail_preview.html')


class ViewMethodsTest(TestCase):

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


    def test_redirect_if_not_logged_in_close_and_reopen(self):
        response = self.client.get(reverse('milestones:close', kwargs={'id': self.MILE1_ID}))
        self.assertRedirects(response, '/?next=/milestones/' + str(self.MILE1_ID) + '/close/')

        response = self.client.get(reverse('milestones:reopen', kwargs={'id': self.MILE1_ID}))
        self.assertRedirects(response, '/?next=/milestones/' + str(self.MILE1_ID) + '/reopen/')

    def test_logged_in_close_and_reopen(self):
        login = self.client.login(username="pera", password="pera1234")
        response = self.client.get(reverse('milestones:close', kwargs={'id': self.MILE1_ID}))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('milestones:reopen', kwargs={'id': self.MILE1_ID}))
        self.assertEqual(response.status_code, 302)
