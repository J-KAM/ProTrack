from django.contrib.auth.models import User
from django.test import TestCase

from django.urls import reverse

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

