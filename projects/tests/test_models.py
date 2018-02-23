from django.contrib.auth.models import User
from django.test import TestCase

from organizations.models import Organization
from projects.models import Project


class ProjectModelTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create(username='pera', email='pera@gmail.com', password='pera1234',first_name='Pera',last_name='Peric')
        self.USER1_ID = test_user1.id

        test_user2 = User.objects.create(username='zika', email='zika@gmail.com', password='zikinasifra',first_name='Zika', last_name='Zikic')
        self.USER2_ID = test_user2.id

        test_organization1 = Organization.objects.create(name='JKAM', owner=test_user1)
        self.ORG1_ID = test_organization1.id

        test_project1 = Project.objects.create(name='First project', url='localhost:8000/pera/First project',description='my first project', created='2018-02-01', num_of_stars=0,owner=test_user1, organization_owner=None, git_owner=None, git_name=None)
        test_project2 = Project.objects.create(name='MySecond', url='localhost:8000/JKAM/MySecond', description='my second project', created='2018-01-15', num_of_stars=0,owner=None, organization_owner=test_organization1, git_owner='J-KAM', git_name='TransportTracker')
        test_project3 = Project.objects.create(name='Treci', url='localhost:8000/zika/First project', description='zikin first project', created='2018-01-25', num_of_stars=0,owner=test_user2, organization_owner=None, git_owner=None, git_name=None)

        self.PRO1_ID = test_project1.id
        self.PRO2_ID = test_project2.id
        self.PRO3_ID = test_project3.id

    def test_field_labels(self):
        project = Project.objects.get(id=self.PRO1_ID)
        name_label = project._meta.get_field('name').verbose_name
        url_label = project._meta.get_field('url').verbose_name
        description_label = project._meta.get_field('description').verbose_name
        created_label = project._meta.get_field('created').verbose_name
        num_of_stars_label = project._meta.get_field('num_of_stars').verbose_name
        owner_label = project._meta.get_field('owner').verbose_name
        organization_owner_label = project._meta.get_field('organization_owner').verbose_name
        git_owner_label = project._meta.get_field('git_owner').verbose_name
        git_name_label = project._meta.get_field('git_name').verbose_name

        self.assertEqual(name_label, 'name')
        self.assertEqual(url_label, 'url')
        self.assertEqual(description_label, 'description')
        self.assertEqual(created_label, 'created')
        self.assertEqual(num_of_stars_label, 'num of stars')
        self.assertEqual(owner_label, 'owner')
        self.assertEqual(organization_owner_label, 'organization owner')
        self.assertEqual(git_owner_label, 'git owner')
        self.assertEqual(git_name_label, 'git name')

    def test_field_nullable(self):
        project = Project.objects.get(id=self.PRO1_ID)
        name_nullable = project._meta.get_field('name').null
        url_nullable = project._meta.get_field('url').null
        description_nullable = project._meta.get_field('description').null
        created_nullable = project._meta.get_field('created').null
        num_of_stars_nullable = project._meta.get_field('num_of_stars').null
        owner_nullable = project._meta.get_field('owner').null
        organization_owner_nullable = project._meta.get_field('organization_owner').null
        git_owner_nullable = project._meta.get_field('git_owner').null
        git_name_nullable = project._meta.get_field('git_name').null

        self.assertFalse(name_nullable)
        self.assertFalse(url_nullable)
        self.assertTrue(description_nullable)
        self.assertFalse(created_nullable)
        self.assertFalse(num_of_stars_nullable)
        self.assertTrue(owner_nullable)
        self.assertTrue(organization_owner_nullable)
        self.assertTrue(git_owner_nullable)
        self.assertTrue(git_name_nullable)

    def test_default_values(self):
        project = Project.objects.get(id=self.PRO1_ID)
        num_of_stars_default = project._meta.get_field('num_of_stars').default
        self.assertEqual(num_of_stars_default, 0)

    def test_max_lengths(self):
        project = Project.objects.get(id=self.PRO1_ID)
        name_max_length = project._meta.get_field('name').max_length
        git_owner_max_length = project._meta.get_field('git_owner').max_length
        git_name_max_length = project._meta.get_field('git_name').max_length

        self.assertEqual(name_max_length, 80)
        self.assertEqual(git_owner_max_length, 255)
        self.assertEqual(git_name_max_length, 255)

    def test_object_name(self):
        project = Project.objects.get(id=self.PRO1_ID)
        self.assertEqual('First project', str(project))

    def test_is_git(self):
        project1 = Project.objects.get(id=self.PRO1_ID)
        project2 = Project.objects.get(id=self.PRO2_ID)

        self.assertFalse(project1.is_git)
        self.assertTrue(project2.is_git)

    def test_name_values(self):
        project1 = Project.objects.get(id=self.PRO1_ID)
        project2 = Project.objects.get(id=self.PRO2_ID)
        project3 = Project.objects.get(id=self.PRO3_ID)

        self.assertEqual(project1.name, 'First project')
        self.assertEqual(project2.name, 'MySecond')
        self.assertEqual(project3.name, 'Treci')

    def test_url_values(self):
        project1 = Project.objects.get(id=self.PRO1_ID)
        project2 = Project.objects.get(id=self.PRO2_ID)
        project3 = Project.objects.get(id=self.PRO3_ID)

        self.assertEqual(project1.url, 'localhost:8000/pera/First project')
        self.assertEqual(project2.url, 'localhost:8000/JKAM/MySecond')
        self.assertEqual(project3.url, 'localhost:8000/zika/First project')

    def test_owner_values(self):
        user1 = User.objects.get(id=self.USER1_ID)
        project1 = Project.objects.get(id=self.PRO1_ID)
        user2 = User.objects.get(id=self.USER2_ID)
        project2 = Project.objects.get(id=self.PRO2_ID)
        organization1 = Organization.objects.get(id=self.ORG1_ID)
        project3 = Project.objects.get(id=self.PRO3_ID)

        self.assertEqual(project1.owner, user1)
        self.assertEqual(project1.organization_owner, None)
        self.assertEqual(project2.owner, None)
        self.assertEqual(project2.organization_owner, organization1)
        self.assertEqual(project3.owner, user2)
        self.assertEqual(project3.organization_owner, None)

