from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from organizations.models import Organization


class OrganizationFormViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('organizations:create'))
        self.assertRedirects(response, '/?next=/organizations/new/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='pera', password='pera1234')
        response = self.client.get(reverse('organizations:create'))

        self.assertEqual(str(response.context['user']), 'pera')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizations/organization_form.html')

    def test_organization_creating(self):
        organization_data = {
            'name': 'My organization',
            'description': 'this is my organization'
        }

        login = self.client.login(username='pera', password='pera1234')
        response = self.client.post(reverse('organizations:create'), organization_data)
        self.assertEqual(response.status_code, 302)


class OrganizationUpdateViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        self.USER1_ID = test_user1.id

        test_org1 = Organization.objects.create(name='JKAM', owner=test_user1, description="desc JKAM")
        self.ORG1_ID = test_org1.id

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('organizations:update', kwargs={'id': self.ORG1_ID}))
        self.assertRedirects(response, '/?next=/organizations/' + str(self.ORG1_ID) + '/')

    def test_logged_in(self):
        login = self.client.login(username="pera", password="pera1234")
        response = self.client.get(reverse('organizations:update', kwargs={'id': self.ORG1_ID}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizations/organization_form.html')

    def test_organization_update(self):
        login = self.client.login(username="pera", password="pera1234")

        organization_data = {
            'name': 'JKAM',
            'description': 'updated description of JKAM',

        }

        response = self.client.post(reverse('organizations:update', kwargs={'id': self.ORG1_ID}), organization_data)
        self.assertEqual(response.status_code, 302)

        organization = Organization.objects.get(id=self.ORG1_ID)
        self.assertEqual(organization.description, 'updated description of JKAM')


class OrganizationPreviewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/organizations/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('organizations:preview'))
        self.assertEqual(response.status_code, 302)
