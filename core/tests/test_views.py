from django.test import TestCase
from django.urls import reverse


class UserFormViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('core:registration'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('core:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/registration_form.html')

    def test_user_registration(self):
        user_data = {
            'username': 'baki',
            'email': 'baki@gmail.com',
            'password': 'baki123',
            'first_name': 'Baki',
            'last_name': 'Bakic'
        }
        response = self.client.post('/register', user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/registration_form.html')


class SignInFormView(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('core:sign_in'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('core:sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signin_form.html')
