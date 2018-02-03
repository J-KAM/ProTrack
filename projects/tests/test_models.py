from django.contrib.auth.models import User
from django.test import TestCase

from organizations.models import Organization
from projects.models import Project

class ProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera',last_name='Peric')
        test_user1.save()
        test_user2 = User.objects.create(username='zika', email='zika@gmail.com', password='zikinasifra',first_name='Zika', last_name='Zikic')
        test_user2.save()

        test_organization1 = Organization.objects.create(name='JKAM', owner=test_user1)

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',description='my first project', created='2018-02-01', num_of_stars=0,owner=test_user1, organization_owner=None)
        test_project2 = Project.objects.create(name='MySecond', url='localhost:8000/JKAM/MySecond', description='my second project', created='2018-01-15', num_of_stars=0,owner=None, organization_owner=test_organization1)
        test_project3 = Project.objects.create(name='Treci', url='localhost:8000/zika/First project', description='zikin first project', created='2018-01-25', num_of_stars=0,owner=test_user2, organization_owner=None)

    def test_field_labels(self):
        project = Project.objects.get(id=1)
        name_label = project._meta.get_field('name').verbose_name
        url_label = project._meta.get_field('url').verbose_name
        description_label = project._meta.get_field('description').verbose_name
        created_label = project._meta.get_field('created').verbose_name
        num_of_stars_label = project._meta.get_field('num_of_stars').verbose_name
        owner_label = project._meta.get_field('owner').verbose_name
        organization_owner_label = project._meta.get_field('organization_owner').verbose_name

        self.assertEquals(name_label, 'name')
        self.assertEquals(url_label, 'url')
        self.assertEquals(description_label, 'description')
        self.assertEquals(created_label, 'created')
        self.assertEquals(num_of_stars_label, 'num of stars')
        self.assertEquals(owner_label, 'owner')
        self.assertEquals(organization_owner_label, 'organization owner')

    def test_field_nullable(self):
        project = Project.objects.get(id=1)
        name_nullable = project._meta.get_field('name').null
        url_nullable = project._meta.get_field('url').null
        description_nullable = project._meta.get_field('description').null
        created_nullable = project._meta.get_field('created').null
        num_of_stars_nullable = project._meta.get_field('num_of_stars').null
        owner_nullable = project._meta.get_field('owner').null
        organization_owner_nullable = project._meta.get_field('organization_owner').null

        self.assertFalse(name_nullable)
        self.assertFalse(url_nullable)
        self.assertTrue(description_nullable)
        self.assertFalse(created_nullable)
        self.assertFalse(num_of_stars_nullable)
        self.assertTrue(owner_nullable)
        self.assertTrue(organization_owner_nullable)

    def test_default_values(self):
        project = Project.objects.get(id=1)
        num_of_stars_default = project._meta.get_field('num_of_stars').default
        self.assertEquals(num_of_stars_default, 0)

    def test_name_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('name').max_length
        self.assertEquals(max_length, 80)

    def test_object_name(self):
        project = Project.objects.get(id=1)
        self.assertEquals('First project', str(project))

    def test_name_values(self):
        project1 = Project.objects.get(id=1)
        project2 = Project.objects.get(id=2)
        project3 = Project.objects.get(id=3)

        self.assertEquals(project1.name, 'First project')
        self.assertEquals(project2.name, 'MySecond')
        self.assertEquals(project3.name, 'Treci')

    def test_url_values(self):
        project1 = Project.objects.get(id=1)
        project2 = Project.objects.get(id=2)
        project3 = Project.objects.get(id=3)

        self.assertEquals(project1.url, 'localhost:8000/pera/First project')
        self.assertEquals(project2.url, 'localhost:8000/JKAM/MySecond')
        self.assertEquals(project3.url, 'localhost:8000/zika/First project')

    def test_owner_values(self):
        user1 = User.objects.get(username="pera")
        project1 = Project.objects.get(id=1)
        user2 = User.objects.get(username="zika")
        project2 = Project.objects.get(id=2)
        organization1 = Organization.objects.get(name="JKAM")
        project3 = Project.objects.get(id=3)

        self.assertEquals(project1.owner, user1)
        self.assertEquals(project1.organization_owner, None)
        self.assertEquals(project2.owner, None)
        self.assertEquals(project2.organization_owner, organization1)
        self.assertEquals(project3.owner, user2)
        self.assertEquals(project3.organization_owner, None)



