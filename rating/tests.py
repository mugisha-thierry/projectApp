from django.test import TestCase
from .models import Profile,Project,Rate

class ProjectTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.picture= Project(title = 'project1',project_pic = 'dsfsd.jpg', description ='a project ',project_link = 'http//www.project.com', date ='2021-11-22',user = 'Profile.user')

    def test_instance(self):
        self.assertTrue(isinstance(self.picture,Project))

    def test_save_method(self):
        self.picture.save_project() 
        projects = Project.objects.all()  
        self.assertTrue(len(projects) > 0) 

    def test_delete_project(self):
        self.picture.save_project()
        self.picture= Image(title = 'project1',project_pic = 'dsfsd.jpg', description ='a project ',project_link = 'http//www.project.com', date ='2021-11-22',user = 'Profile.user')
        self.picture.save_project()
        self.picture.delete_project()
        deleted = Project.objects.all()
        self.assertEqual(len(deleted),1)
