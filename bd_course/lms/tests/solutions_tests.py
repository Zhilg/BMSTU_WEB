from django.test import TestCase
from lms.managers.managers import SolutionsManager, TaskPacksManager, UserProfilesManager, TasksManager
from lms.exceptions import *
from datetime import date

class SolutionsTests(TestCase):
    def setUp(self):
        form1 = {"N" : 1, "group" : "IU7-61B", "theme" : "Mathematics", "duetime" : date(2023, 10, 3)}
        form2 = {'email' : '124@mail.ru', "password" : "asdasdasd", "username" : "bruh", "group" : "Teacher"}
        teacher = UserProfilesManager().create(form=form2)
        
        
        form2 = {'email' : '125@mail.ru', "password" : "asdasdasd", "username" : "bruh2", "group" : "IU7-61B"}
        self.user = UserProfilesManager().create(form=form2)
        
        form = {"filename" : "asdasdd.txt", "theme" : "Mathematics"}
        TasksManager().create(form)
        
        self.taskpack = TaskPacksManager().create(form1, teacher)
        
        self.test_form_1 = {"filename" : "a.txt", "taskpackid" : self.taskpack[0].id}
        self.test_form_2 = {"filename" : "a.txt", "taskpackid" : self.taskpack[0].id}
        self.test_form_3 = {"filename" : "b.txt", "taskpackid" : 1000}
        self.test_form_4 = {"filename" : "c.txt", "taskpackid" : self.taskpack[0].id}
        
    def test_create_solution(self):
        solution = SolutionsManager().create(self.user, self.test_form_1)
        self.assertIsInstance(solution, SolutionsManager().model)
        
    def test_file_exists(self):
        try:
            SolutionsManager().create(self.user, self.test_form_2)
        except FileAlreadyExists:
            self.assertTrue(True)
            
    def test_no_taskpack(self):
        try:
            SolutionsManager().create(self.user, self.test_form_3)
        except NoSuchTaskPacks:
            self.assertTrue(True)
            
    def test_wrong_taskpack(self):
        form = {'email' : '126@mail.ru', "password" : "asdasdasd", "username" : "bruh2", "group" : "IU7-71B"}
        user = UserProfilesManager().create(form=form)
        try:
            SolutionsManager().create(user, self.test_form_4)
        except WrongTaskPackID:
            self.assertTrue(True)
        