from django.test import TestCase

from organizations.forms import OrganizationForm


class OrganizationFromTest(TestCase):

    def test_field_labels(self):
        form = OrganizationForm()

        self.assertEqual(form['name'].label, 'Name')
        self.assertEqual(form['description'].label, 'Description')
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Description')

    def test_required_fields(self):
        form = OrganizationForm()

        self.assertTrue(form.fields['name'].required)
        self.assertFalse(form.fields['description'].required)

    def test_field_number(self):
        form = OrganizationForm()

        self.assertEquals(len(form.fields), 2)

    def test_invalid_form(self):
        form_data = {
            # name is required
            'description': 'opis projekta'
        }

        form = OrganizationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        form_data = {
            'name': 'Organization One',
            'description': 'Description of organization one'

        }

        form = OrganizationForm(data=form_data)
        self.assertTrue(form.is_valid())
