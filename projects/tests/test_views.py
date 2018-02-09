from django.contrib.auth.models import User
from django.test import TestCase

from django.urls import reverse

from projects.models import Project


class ProjectCreateFormViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('projects:create'))
        self.assertRedirects(response, '/?next=/projects/new/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get(reverse('projects:create'))

        self.assertEqual(str(response.context['user']), 'pera')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_form.html')

    def test_project_creating(self):
        project_data = {
            'name': 'My project',
            'owner_type': 'm',
            'description': 'this is my project'
        }

        login = self.client.login(username='pera', password='pera1234')
        response = self.client.post(reverse('projects:create'), project_data)
        self.assertEqual(response.status_code, 302)


class ProjectUpdateFormViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',description='my first project', created='2018-02-01', num_of_stars=0,owner=test_user1, organization_owner=None)
        self.PRO1_ID = test_project1.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('projects:update', kwargs={'id': self.PRO1_ID}))
        self.assertRedirects(response, '/?next=/projects/' + str(self.PRO1_ID) + '/')
