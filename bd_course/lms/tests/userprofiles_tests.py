from django.test import TestCase
from lms.managers.managers import UserProfilesManager

# Create your tests here.
class UserProfilesTests(TestCase):
    def setUp(self):
        form = {'email' : '124@mail.ru', "password" : "asdasdasd", "username" : "bruh", "group" : "Teacher"}
        UserProfilesManager().create(form=form)
    
    def test_get(self):
        prof = UserProfilesManager().get_user_by_email(email='124@mail.ru')
        self.assertIsInstance(prof, UserProfilesManager().model)
    
    def test_ch_pas(self):
        form = {"old_password" : "asdasdasd", "new_password" : "12345678"}
        prof = UserProfilesManager().get_user_by_email(email='124@mail.ru')
        UserProfilesManager().change_password(form, prof)
        self.assertTrue(prof.check_password(form["new_password"]))
        