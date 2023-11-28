from django.contrib.auth.backends import BaseBackend
from lms.boot import UPM

class EmailBackend(BaseBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        
        user = UPM.get(email=email)[0]
        print(user)
        if user is None:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return UPM.get(id=user_id).first()

        except UPM.rep.model.DoesNotExist:
            return None