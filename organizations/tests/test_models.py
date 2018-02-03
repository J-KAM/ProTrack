from django.contrib.auth.models import User
from django.test import TestCase

from organizations.models import Organization


class OrganizationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',
                                              first_name='Pera', last_name="Peric")
        test_user1.save()
        test_user2 = User.objects.create_user(username='mika', email='mika@gmail.com', password='mika333',
                                              first_name='Mika', last_name="Mikic")
        test_user2.save()

        test_org1 = Organization.objects.create(name='JKAM', owner=test_user1, description="desc JKAM")
        test_org2 = Organization.objects.create(name='MAJK', owner=test_user2, description="desc MAJK")

    def test_field_labels(self):
        organization = Organization.objects.get(id=1)
        name_label = organization._meta.get_field('name').verbose_name
        description_label = organization._meta.get_field('description').verbose_name
        owner_label = organization._meta.get_field('owner').verbose_name

        self.assertEquals(name_label, 'name')
        self.assertEquals(description_label, 'description')
        self.assertEquals(owner_label, 'owner')

    def test_field_nullable(self):
        organization = Organization.objects.get(id=1)
        name_nullable = organization._meta.get_field('name').null
        description_nullable = organization._meta.get_field('description').null
        owner_nullable = organization._meta.get_field('owner').null

        self.assertFalse(name_nullable)
        self.assertTrue(description_nullable)
        self.assertFalse(owner_nullable)

    def test_name_max_length(self):
        organization = Organization.objects.get(id=1)
        max_length = organization._meta.get_field('name').max_length
        self.assertEquals(max_length, 80)

    def test_object_name(self):
        organization = Organization.objects.get(id=1)
        self.assertEquals('JKAM', str(organization))

    def test_name_values(self):
        organization1 = Organization.objects.get(id=1)
        organization2 = Organization.objects.get(id=2)

        self.assertEquals(organization1.name, 'JKAM')
        self.assertEquals(organization2.name, 'MAJK')

    def test_owner_values(self):
        user1 = User.objects.get(username="pera")
        organization1 = Organization.objects.get(name="JKAM")  # id 1
        user2 = User.objects.get(username="mika")
        organization2 = Organization.objects.get(name="MAJK")  # id 2

        self.assertEquals(organization1.owner, user1)
        self.assertEquals(organization2.owner, user2)
