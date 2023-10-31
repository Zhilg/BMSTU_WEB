from django.contrib.auth.backends import BaseBackend
from lms.repositories.repositories import UserProfilesRepository

class EmailBackend(BaseBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        
        user = UserProfilesRepository().model.objects.filter(email=email).first()
        print(user)
        if user is None:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return UserProfilesRepository().model.objects.filter(pk=user_id).first()

        except UserProfilesRepository().model.DoesNotExist:
            print("MODEL DOES NOT EXIST\n\n")
            return None