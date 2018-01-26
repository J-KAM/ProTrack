from django.contrib.auth.models import User
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


class SignInFormViewTest(TestCase):

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


class UserUpdateFormViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',
                                 first_name='Pera', last_name="Peric")
        test_user1.save()
        test_user1 = User.objects.create_user(username='mika', email='mika@gmail.com', password='mika333',
                                 first_name='Mika', last_name="Mikic")
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('core:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in(self):
        login = self.client.login(username="pera", password="pera1234")
        response = self.client.get(reverse('core:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/profile_form.html')


    def test_user_update(self):
        login = self.client.login(username="pera", password="pera1234")

        user_data = {
            'first_name': 'Petar',
            'last_name': 'Peric',
            'email': 'pera@gmail.com',

        }

        response = self.client.post(reverse('core:profile'), user_data)
        self.assertEqual(response.status_code, 200)

        user1 = User.objects.get(username="pera")
        self.assertEqual(user1.first_name, 'Petar')
        self.assertTemplateUsed(response, 'core/profile_form.html')

    def test_user_update_failure1(self):
        # missing last name - > failure
        login = self.client.login(username="pera", password="pera1234")

        user_data = {
            'first_name': 'Petar',
            'email': 'pera@gmail.com',

        }

        response = self.client.post(reverse('core:profile'), user_data)
        self.assertEqual(response.status_code, 200)

        user1 = User.objects.get(username="pera")
        self.assertNotEqual(user1.first_name, 'Petar')
        self.assertTemplateUsed(response, 'core/profile_form.html')

    def test_user_update_failure2(self):
        # email already in use- > failure
        login = self.client.login(username="pera", password="pera1234")

        user_data = {
            'first_name': 'Petar',
            'last_name': 'Peric',
            'email': 'mika@gmail.com',

        }

        response = self.client.post(reverse('core:profile'), user_data)
        self.assertEqual(response.status_code, 200)

        user1 = User.objects.get(username="pera")
        self.assertNotEqual(user1.email, 'mika@gmail.com')
        self.assertTemplateUsed(response, 'core/profile_form.html')
        self.assertEqual(response.context['error_message'], 'This email address is already in use. Please supply a different email address.')

    def test_change_password(self):
        login = self.client.login(username="pera", password="pera1234")

        user_data = {
            'old_password': 'pera1234',
            'new_password1': 'peki1234',
            'new_password2': 'peki1234',

        }

        response = self.client.post(reverse('core:change_password'), user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/home/profile/password'))

    def test_change_password_failure(self):
        login = self.client.login(username="pera", password="pera1234")

        user_data = {
            'old_password': 'peki', # incorrect old password
            'new_password1': 'peki1234',
            'new_password2': 'peki1234',

        }

        response = self.client.post(reverse('core:change_password'), user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/change_password.html')


    def test_get_home_page(self):
        # test when user is not logged in
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

        # test when user is logged in
        login = self.client.login(username="pera", password="pera1234")
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home_page.html')