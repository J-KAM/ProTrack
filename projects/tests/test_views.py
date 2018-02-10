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

    def test_protrack_project_creating(self):
        project_data = {
            'name': 'My project',
            'project_type': 'p',
            'owner_type': 'm',
            'description': 'this is my project'
        }

        login = self.client.login(username='pera', password='pera1234')
        response = self.client.post(reverse('projects:create'), project_data)
        self.assertEqual(response.status_code, 200)

    def test_github_project_creating(self):
        project_data = {
            'name': 'My project',
            'project_type': 'g',
            'git_owner': 'J-KAM',
            'git_name': 'GitProject',
            'owner_type': 'm',
            'description': 'this is my project'
        }

        login = self.client.login(username='pera', password='pera1234')
        response = self.client.post(reverse('projects:create'), project_data)
        self.assertEqual(response.status_code, 200)


class ProjectUpdateFormViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',description='my first project', created='2018-02-01', num_of_stars=0,owner=test_user1, organization_owner=None, git_owner=None, git_name=None)
        self.PRO1_ID = test_project1.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('projects:update', kwargs={'id': self.PRO1_ID}))
        self.assertRedirects(response, '/?next=/projects/' + str(self.PRO1_ID) + '/')

    def test_logged_in(self):
        login = self.client.login(username="pera", password="pera1234")
        response = self.client.get(reverse('projects:update', kwargs={'id': self.PRO1_ID}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_form.html')

    def test_protrack_project_update(self):
        login = self.client.login(username="pera", password="pera1234")

        project_data = {
            'name': 'New project name',
            'project_type': 'p',
            'description': 'this is my project'
        }
        response = self.client.post(reverse('projects:update', kwargs={'id': self.PRO1_ID}), project_data)
        self.assertEqual(response.status_code, 302)

        project = Project.objects.get(id=self.PRO1_ID)
        self.assertEqual(project.name, 'New project name')
