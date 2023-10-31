from bd_course.BaseRep import BaseRep
from lms.models.models import *
from lms.exceptions import *
from random import choices
from datetime import date

class UserProfilesRepository(BaseRep):
    def __init__(self):
        self.model = UserProfiles
        
    def get(self, user_id=None, email=None):
        if user_id is not None:
            return self.model.objects.filter(pk=user_id)
        if email is not None:
            return self.model.objects.filter(email=email)
        

    def update(self, form, user):
        old = form['old_password']
        new = form['new_password']
        if user.check_password(old):
            user.set_password(new)
            user.save()
            return user
        else:
            raise ValueError
    
    def insert(self, form, **extra_fields):
        email = form['email']
        username = form['username']
        grup = form['group']
        password = form['password']
        
        user = self.model(
        email=email,
        username=username,
        grup=grup,
        **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
class TasksRepository(BaseRep):
    def __init__(self):
        self.model = Tasks
        
    def insert(self, form):
        task = self.model(theme=form['theme'], filename=form['filename'])
        task.save()
        return task
    
    def update(self, form):
        pass
    
    def get(self, filename):
        return self.model.objects.filter(filename=filename)
        
    
class TaskPacksRepository(BaseRep):
    def __init__(self):
        self.model = TaskPacks
        
    def get(self, teacher=None, student=None, id=None):
        if teacher is not None:
            return self.model.objects.filter(teacher=teacher)
        if student is not None:
            return self.model.objects.filter(student=student)
        if id is not None:
            return self.model.objects.filter(pk=id)
    
    def update(self, form):
        pass
        
    def insert(self, form, user):
        N = form['N']
        if N <= 0:
            raise NonPositiveNException
            
        student_ids = UserProfiles.objects.filter(grup=form['group'])# Все id студентов какой-то группы
        if not student_ids.__len__():
            raise NoSuchGroupException
            
        duetime = form['duetime']
        if duetime < date.today():
            raise WrongDeadlineException       
        
        tasks_ids = list(TasksRepository().model.objects.filter(theme=form['theme']).values_list('id', flat=True)) # Все id заданий на соотв тему
        len = tasks_ids.__len__()
        if len == 0:
            raise NoSuchThemeException
            
        elif len < N:
            raise NotEnoughTasksException
            
        teacher = user
        
        ret_list = []
        
        for student in student_ids:
            pack = self.model(student = student, teacher=teacher, duetime=duetime)
            pack.save()
            ret_list.append(pack)
            pack.tasks.add(*choices(tasks_ids, k=form['N']))
        
        return ret_list
    
class SolutionsRepository(BaseRep):
    def __init__(self) -> None:
        self.model = Solutions
        
    def get(self, teacher=None, student=None):
        if teacher is not None:
            return self.model.objects.filter(teacher=teacher)
        if student is not None:
            return self.model.objects.filter(student=student)
        
    def insert(self, form, user):
        taskpacksid = form['taskpackid']
        filename = form['filename']
        query = self.model.objects.filter(filename=filename)
        if query.__len__():
            raise FileAlreadyExists
            
        query = TaskPacksRepository().get(id=taskpacksid)
        if not query.__len__():
            raise NoSuchTaskPacks
            
        query = TaskPacksRepository().get(student=user).values_list('id', flat=True)
        
        if taskpacksid not in list(query):
            raise WrongTaskPackID
        
        taskpack = TaskPacksRepository().get(id=taskpacksid).first()
        teacher = taskpack.teacher
        solution = self.model(filename=filename, taskpack=taskpack, student=user, teacher=teacher)
        solution.save()
        return solution
    
    def update(self, form):
        id = form.cleaned_data['solutionid']
        solution = self.model.objects.get(id=id)
        grade = form.cleaned_data['grade']
        solution.grade = grade
        solution.save()