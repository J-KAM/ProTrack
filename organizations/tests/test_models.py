from django.contrib.auth.models import User
from django.test import TestCase

from organizations.models import Organization


class OrganizationModelTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='pera', email='pera@gmail.com', password='pera1234',
                                              first_name='Pera', last_name="Peric")
        self.USER1_ID = test_user1.id
        test_user2 = User.objects.create_user(username='mika', email='mika@gmail.com', password='mika333',
                                              first_name='Mika', last_name="Mikic")
        self.USER2_ID = test_user2.id

        test_org1 = Organization.objects.create(name='JKAM', owner=test_user1, description="desc JKAM")
        test_org2 = Organization.objects.create(name='MAJK', owner=test_user2, description="desc MAJK")

        self.ORG1_ID = test_org1.id
        self.ORG2_ID = test_org2.id

    def test_field_labels(self):
        organization = Organization.objects.get(id=self.ORG1_ID)
        name_label = organization._meta.get_field('name').verbose_name
        description_label = organization._meta.get_field('description').verbose_name
        owner_label = organization._meta.get_field('owner').verbose_name

        self.assertEquals(name_label, 'name')
        self.assertEquals(description_label, 'description')
        self.assertEquals(owner_label, 'owner')

    def test_field_nullable(self):
        organization = Organization.objects.get(id=self.ORG1_ID)
        name_nullable = organization._meta.get_field('name').null
        description_nullable = organization._meta.get_field('description').null
        owner_nullable = organization._meta.get_field('owner').null

        self.assertFalse(name_nullable)
        self.assertTrue(description_nullable)
        self.assertFalse(owner_nullable)

    def test_name_max_length(self):
        organization = Organization.objects.get(id=self.ORG1_ID)
        max_length = organization._meta.get_field('name').max_length
        self.assertEquals(max_length, 80)

    def test_object_name(self):
        organization = Organization.objects.get(id=self.ORG1_ID)
        self.assertEquals('JKAM', str(organization))

    def test_name_values(self):
        organization1 = Organization.objects.get(id=self.ORG1_ID)
        organization2 = Organization.objects.get(id=self.ORG2_ID)

        self.assertEquals(organization1.name, 'JKAM')
        self.assertEquals(organization2.name, 'MAJK')

    def test_owner_values(self):
        user1 = User.objects.get(id=self.USER1_ID)
        organization1 = Organization.objects.get(id=self.ORG1_ID)
        user2 = User.objects.get(id=self.USER2_ID)
        organization2 = Organization.objects.get(id=self.ORG2_ID)

        self.assertEquals(organization1.owner, user1)
        self.assertEquals(organization2.owner, user2)
