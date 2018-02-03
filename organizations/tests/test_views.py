from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from organizations.models import Organization


class OrganizationFormViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
        test_user1.save()

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
        test_user1.save()
        test_org1 = Organization.objects.create(name='JKAM', owner=test_user1, description="desc JKAM")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('organizations:update', kwargs={'id':1}))
        self.assertRedirects(response, '/?next=/organizations/1/')

    def test_logged_in(self):
        login = self.client.login(username="pera", password="pera1234")
        response = self.client.get(reverse('organizations:update', kwargs={'id': 4}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizations/organization_form.html')

    def test_organization_update(self):
        login = self.client.login(username="pera", password="pera1234")

        organization_data = {
            'name': 'JKAM',
            'description': 'updated description of JKAM',

        }

        response = self.client.post(reverse('organizations:update', kwargs={'id':5 }), organization_data)
        self.assertEqual(response.status_code, 302)

        organization = Organization.objects.get(id=5)
        self.assertEqual(organization.description, 'updated description of JKAM')


class OrganizationPreviewTest(TestCase):

    # @classmethod
    # def setUp(cls):
    #     num_of_organizations = 5
    #     test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera', last_name='Peric')
    #     test_user1.save()
    #
    #     for org_num in range(num_of_organizations):
    #         Organization.objects.create(name='Org %s' %org_num, owner=test_user1, description="desc of org %s" %org_num)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/organizations/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('organizations:preview'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('organizations:preview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizations/preview.html')




