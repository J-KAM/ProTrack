from django.test import TestCase

from core.forms import UserForm, SignInForm


class UserFormTest(TestCase):

    def test_first_name_field_label(self):
        form = UserForm()

        self.assertEqual(form['first_name'].label, 'First name')
        self.assertTrue(form.fields['first_name'].label is None or form.fields['first_name'].label == 'First name')

    def test_valid_user_form(self):
        form_data = {
            'username': 'niki',
            'email': 'niki@gmail.com',
            'password': 'niki123',
            'first_name': 'Nikola',
            'last_name': 'Nikolic'
        }

        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_form(self):
        form_data = {
            'username': 'miki',
            'email': 'miki@gmail.com',
            'password': 'miki123',
            'first_name': 'Milan',
            # last name is required
        }

        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())


class SignInFormTest(TestCase):

    def test_valid_sign_in_form(self):

        form_data = {
            'username': 'niki',
            'password': 'niki123',
        }

        form = SignInForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_sign_in_form(self):
        form_data = {
            'username': 'niki',
        }

        form = SignInForm(data=form_data)
        self.assertFalse(form.is_valid())
