from django.test import TestCase
from lms.boot import *
from lms.exceptions import *
from datetime import date

class SolutionsTests(TestCase):
    def setUp(self):
        form1 = {"n" : 1, "group" : "IU7-61B", "theme" : "Mathematics", "duetime" : date.today(), 'maxgrade':10, "mingrade":1}
        form2 = {'email' : '124@mail.ru', "password" : "asdasdasd", "username" : "bruh", "grup" : "Teacher"}
        teacher = UPM.create(form=form2)
        
        form2 = {'email' : '125@mail.ru', "password" : "asdasdasd", "username" : "bruh2", "grup" : "IU7-61B"}
        self.user = UPM.create(form=form2)
        
        form = {"filename" : "asdasdd.txt", "theme" : "Mathematics"}
        TM.create(form)
        
        self.taskpack = TPM.create(form1, teacher)
        
        self.test_form_1 = {"filename" : "a.txt", "taskpackid" : self.taskpack[0].id}
        self.test_form_2 = {"filename" : "a.txt", "taskpackid" : self.taskpack[0].id}
        self.test_form_3 = {"filename" : "b.txt", "taskpackid" : 1000}
        self.test_form_4 = {"filename" : "c.txt", "taskpackid" : self.taskpack[0].id}
        
    def test_create_solution(self):
        solution = SM.create(self.user, self.test_form_1)
        self.assertIsInstance(solution, SM.model)
        
    def test_file_exists(self):
        try:
            SM.create(self.user, self.test_form_2)
        except FileAlreadyExists:
            self.assertTrue(True)
            
    def test_no_taskpack(self):
        try:
            SM.create(self.user, self.test_form_3)
        except NoSuchTaskPacks:
            self.assertTrue(True)
            
    def test_wrong_taskpack(self):
        form = {'email' : '126@mail.ru', "password" : "asdasdasd", "username" : "bruh2", "group" : "IU7-71B"}
        user = UPM.create(form=form)
        try:
            SM.create(user, self.test_form_4)
        except WrongTaskPackID:
            self.assertTrue(True)
        