
from lms.repositories.repositories import *
from bd_course.BaseManag import BaseUserManag, BaseManag

from lms.exceptions import *
from django.contrib.auth.models import BaseUserManager

# для менеджеров свои модельки, а репозиторий конвертирует из модели в бд в модель для менеджеров
# модели в ОРМ слишком сильно связаны с менеджерами, ослабить эту связь, абстрагироваться
#создавать менеджеров через какойто конструктор, отдельный класс (фабрику), туда передавать связь с репозиторием


class UserProfilesManager(BaseUserManag, BaseUserManager):
    def __init__(self):
        super().__init__()
        self.rep = None
        
    def create(self, form, **extra_fields):
        if self.get(form['email']):
            raise ValueError
        user = self.rep.insert(form, **extra_fields)
        return user

    def create_superuser(self, email, username, grup, password=None, **extra_fields): # зависимость передавать через конструктор
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.rep.insert(email, username, grup, password, **extra_fields)
    
    def get(self, email):
        try:
            return self.rep.get(email)
        except self.rep.model.DoesNotExist:
            return None
        
    def auth_user(self, form, request, backend):
        email = self.normalize_email(form['email'])
        password = form['password']
        print(request.user)
        print("BEFORE BACKEND")
        user = backend.authenticate(request=request, email=email, password=password)
        print(user)
        if user is not None and user.is_active:
            print("logineedddd")
            login(request, user, backend="lms.backends.EmailBackend")
        else:
            raise ValueError
    
    def change_password(self, form, user):
        return self.rep.update(form, user)
        
        

class TasksManager(BaseManag, models.Model):
    def __init__(self):
        super().__init__()
        
        
    def create(self, form):
        query = self.rep.get(form['filename'])
        print(query)
        if query.__len__():
            raise FileAlreadyExists
        return self.rep.insert(form)
        
        
class TaskPacksManager(BaseManag, models.Model):
    def __init__(self):
        super().__init__()
    
    def create(self, form, user):
        return self.rep.insert(form, user)
            
    def get(self, user):
        if user.grup == 'Teacher':
            TASKPACKS_QUERY = list(self.rep.get(teacher=user.id).values())
        else:
            TASKPACKS_QUERY = list(self.rep.get(student=user.id).values())
        return TASKPACKS_QUERY
    
    def unpack_fields_values(self, user):
        TASKPACKS_QUERY = self.get(user)
        return [list(i.values()) for i in TASKPACKS_QUERY]
    
    def get_meta_fields(self):
        return [f.name for f in self.rep.model._meta.get_fields()[1:-1]]
        

class SolutionsManager(BaseManag, models.Model):
    def __init__(self):
        super().__init__()
    
    def create(self, user, form):
        self.rep.insert(form, user)
        
    def update(self, form):
        self.rep.update(form)
        
    def get(self, user):
        if user.grup == 'Teacher':
            SOLUTIONS_QUERY = list(self.rep.get(teacher=user.id).values())
        else:
            SOLUTIONS_QUERY = list(self.rep.get(student=user.id).values())
        return SOLUTIONS_QUERY
    
    def get_meta_fields(self):
        return [f.name for f in self.rep.model._meta.get_fields()]
    
    def unpack_fields_values(self, user):
        query = self.get(user)
        return [list(i.values()) for i in query]