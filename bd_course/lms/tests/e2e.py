from rest_framework.test import APITestCase, APIClient
from lms.tests.builder import *

class E2ETest(APITestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.user_form = {'email' : '125@mail.ru', "password" : "asdasdasd", "username" : "bruh2", "grup" : "teacher"}
        self.user = UserBuilder.create_student()
        self.user.is_authenticated = True

        
    def test_e2e(self):
        response = self.client.get(self.url+"/taskpacks")
        self.assertEqual(response.status_code, 401)
        response = self.client.post(self.url+'/auth/login', data=self.user_form)
        self.client.force_authenticate(user=self.user)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.url+"/taskpacks")
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.url+"/tasks", data={"filename" : "asdasdd.txt", "theme" : "Mathematics"})
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(TM.get("asdasdd.txt")[0], TM.rep.model)
        
        