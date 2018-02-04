from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.


class UserModelTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',
                                              first_name='Pera', last_name="Peric")
        self.USER1_ID = test_user1.id
        test_user2 = User.objects.create_user(username='mika', email='mika@gmail.com', password='mika333',
                                              first_name='Mika', last_name="Mikic")
        self.USER2_ID = test_user2.id

    def test_field_label(self):
        user = User.objects.get(id=self.USER1_ID)
        username_label = user._meta.get_field('username').verbose_name
        password_label = user._meta.get_field('password').verbose_name
        email_label = user._meta.get_field('email').verbose_name
        first_name_label = user._meta.get_field('first_name').verbose_name
        last_name_label = user._meta.get_field('last_name').verbose_name

        self.assertEquals(username_label, 'username')
        self.assertEquals(password_label, 'password')
        self.assertEquals(email_label, 'email address')
        self.assertEquals(first_name_label, 'first name')
        self.assertEquals(last_name_label, 'last name')

    def test_first_name_values(self):
        user1 = User.objects.get(id=self.USER1_ID)
        user2 = User.objects.get(id=self.USER2_ID)

        self.assertEquals(user1.first_name, 'Pera')
        self.assertEquals(user2.first_name, 'Mika')

    def test_last_name_values(self):
        user1 = User.objects.get(id=self.USER1_ID)
        user2 = User.objects.get(id=self.USER2_ID)

        self.assertEquals(user1.last_name, 'Peric')
        self.assertEquals(user2.last_name, 'Mikic')

    def test_username_values(self):
        user1 = User.objects.get(id=self.USER1_ID)
        user2 = User.objects.get(id=self.USER2_ID)

        self.assertEquals(user1.username, 'pera')
        self.assertEquals(user2.username, 'mika')

    def test_email_values(self):
        user1 = User.objects.get(id=self.USER1_ID)
        user2 = User.objects.get(id=self.USER2_ID)

        self.assertEquals(user1.email, 'pera@gmail.com')
        self.assertEquals(user2.email, 'mika@gmail.com')


