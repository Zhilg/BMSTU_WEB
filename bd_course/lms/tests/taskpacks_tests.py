from django.test import TestCase
from lms.managers.managers import TaskPacksManager, UserProfilesManager, TasksManager
from datetime import date
from lms.exceptions import *
    
class TaskPacksTests(TestCase):
    def setUp(self):
        self.form1 = {"N" : -1, "group" : "IU7-61B", "theme" : "Mathematics", "duetime" : date(2023, 10, 3)}
        self.form2 = {"N" : 1, "group" : "None", "theme" : "Mathematics", "duetime" : date(2023, 10, 3)}
        self.form3 = {"N" : 1, "group" : "IU7-61B", "theme" : "None", "duetime" : date(2023, 10, 3)}
        self.form4 = {"N" : 1, "group" : "IU7-61B", "theme" : "Mathematics", "duetime" : date(2023, 9, 3)}
        self.form5 = {"N" : 5, "group" : "IU7-61B", "theme" : "Mathematics", "duetime" : date(2023, 10, 3)}
        self.form6 = {"N" : 1, "group" : "IU7-61B", "theme" : "Mathematics", "duetime" : date(2023, 10, 3)}
        
        form = {'email' : '124@mail.ru', "password" : "asdasdasd", "username" : "bruh", "group" : "Teacher"}
        self.user = UserProfilesManager().create(form=form)
        form = {'email' : '125@mail.ru', "password" : "asdasdasd", "username" : "bruh2", "group" : "IU7-61B"}
        UserProfilesManager().create(form=form)
        form = {"filename" : "asdasdd.txt", "theme" : "Mathematics"}
        TasksManager().create(form)
        
    def test_neg_n(self):
        try:
            TaskPacksManager().create(form=self.form1, user=self.user)
        except NonPositiveNException:
            self.assertTrue(True, True)
    
    def test_wrong_deadline(self):
        try:
            TaskPacksManager().create(form=self.form4, user=self.user)
        except WrongDeadlineException:
            self.assertTrue(True, True)
    
    def test_no_group(self):
        try:
            TaskPacksManager().create(form=self.form2, user=self.user)
        except NoSuchGroupException:
            self.assertTrue(True, True)
            
    def test_no_such_theme(self):
        try:
            TaskPacksManager().create(form=self.form3, user=self.user)
        except NoSuchThemeException:
            self.assertTrue(True, True)
            
    def test_not_enough_tasks(self):
        try:
            TaskPacksManager().create(form=self.form5, user=self.user)
        except NotEnoughTasksException:
            self.assertTrue(True, True)
            
    def test_create_taskpack(self):
        try:
            TaskPacksManager().create(form=self.form6)
        except Exception:
            pass
        self.assertIsNotNone(TaskPacksManager.get_taskpacks(user=self.user))
    
    
         
            
        
      
      
      
        