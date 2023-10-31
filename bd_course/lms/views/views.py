from lms.forms.forms import *
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser

from ..backends import EmailBackend
from lms.boot import *

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            try:
                UPM.create(form=form.clean())
            except ValueError:
                form.add_error(None, 'Такой пользователь уже существует')
        else:
            form.add_error(None, "Форма заполнена неправильно")        
        
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        if form.is_valid():
            try:       
                UPM.auth_user(request=request, form=form.clean(), backend=EmailBackend())
                print(request.user)
                return redirect('/view')
            except ValueError:
                form.add_error(None, 'Incorrect email or password')
        else:
            form.add_error(None, "Форма заполнена неправильно")  
    else:
        form = LoginForm()
        
    return render(request, 'registration/login.html', {'form': form})

def change_password(request):
    print(request.user)
    if request.user == AnonymousUser:
        return redirect('/login')

    if request.method == 'POST':
        
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                print(request.user)
                UPM.change_password(form.clean(), request.user)
                return HttpResponseRedirect('/view')
            except ValueError:
                form.add_error(None, 'Incorrect password')
        else:
            form.add_error(None, "Форма заполнена неправильно")  
    else:
        form = ChangePasswordForm()
    return render(request, 'registration/change_password.html', {'form': form})

def view(request):
    print(request.user)
    return render(request, "view.html")
    
def check(request):
    MODEL_HEADERS=[f.name for f in Tasks._meta.get_fields()[4:]]
    query_results = [list(i.values()) for i in list(Tasks.objects.all().values())]
    return render(request, "view.html", {
            "query_results" : query_results,
            "model_headers" : MODEL_HEADERS
        })
    
def create_taskpacks(request):
    # Может делать только учитель
    # Выбирает группу, и для каждого студента этой группы делается пак заданий темы учителя
    # Входные данные - группа, количество заданий, тема
    if request.user == AnonymousUser or request.user.grup != 'Teacher':
        return HttpResponseRedirect('/view')
    if request.method == 'POST':
        form = CreateTaskPacks(request.POST)
        if form.is_valid():    
            try:
                TPM.create(form.clean(), request.user)
            except NonPositiveNException:
                form.add_error(None, 'Количество заданий в комплекте не может быть <= 0')
            except NoSuchGroupException:
                form.add_error(None, 'Такой группы нет в системе')
            except WrongDeadlineException:
                form.add_error("Неправильный дедлайн данных комплектов")
            except NoSuchThemeException:
                form.add_error(None, 'Заданий с такой темой нет в системе')
            except NotEnoughTasksException:
                form.add_error(None, 'Недостаточно заданий в системе для формирования комплекта, текущее количество заданий =  {}'.format(len))

        else:
            form.add_error(None, 'Форма заполнена неправильно')
    else:
        form = CreateTaskPacks()
        HttpResponseRedirect(request.META.get('HTTP_REFERER').replace('/create_taskpacks?', ''))
    return render(request, 'create_taskpacks.html', {'form': form})

def show_taskpacks(request):
    if request.user != AnonymousUser:
        
        TASKPACKS_HEADER, TASKPACKS_QUERY = TPM.get_meta_fields(), TPM.unpack_fields_values(user=request.user)
        print(TASKPACKS_HEADER, TASKPACKS_QUERY)
        return render(request, "showtable.html", {
                    "query_results" : TASKPACKS_QUERY,
                    "model_headers" : TASKPACKS_HEADER
                })
            
    return HttpResponse('У анонимного пользователя нет никаких комплектов')
        
def show_solutions(request):
    if request.user != AnonymousUser:
        SOLUTIONS_HEADER, SOLUTIONS_QUERY = SM.get_meta_fields(), SM.unpack_fields_values(user=request.user)
        return render(request, "showtable.html", {
                "query_results" : SOLUTIONS_QUERY,
                "model_headers" : SOLUTIONS_HEADER
            })
    return HttpResponse('bruh')

def upload_solutions(request):
    if request.user == AnonymousUser or request.user.grup == 'Teacher':
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        form = UploadSolutions(request.POST)
        if form.is_valid():
            try:
                SM.create(request.user, form.clean())
            except FileAlreadyExists:
                form.add_error(None, "Файл с таким названием уже существует в системе")
            except NoSuchTaskPacks:
                form.add_error(None, "Данного комплекта заданий не существует")
            except WrongTaskPackID:
                form.add_error(None, "Данный комплект заданий не ваш")  
        else:
            form.add_error(None, "Форма заполнена неправильно")                     
    else:
        form = UploadSolutions()
    return render(request, 'upload_solutions.html', {'form': form})

    
def upload_tasks(request):
    if request.user == AnonymousUser or request.user.grup != 'Teacher':
        return HttpResponseRedirect('/login')
    
    if request.method == 'POST':
        form = UploadTask(request.POST)
        if form.is_valid():
            try:
                TM.create(form.clean())
            except FileAlreadyExists:
                form.add_error(None, "Файл с таким названием уже существует в системе")
        else:
            form.add_error(None, "Форма заполнена неправильно")  
    else:
        form = UploadTask()
    return render(request, 'upload_tasks.html', {'form': form})

def grade_solutions(request):
    if request.user.grup != 'Teacher':
        return HttpResponseRedirect('/login')

    header, query = SM.get_meta_fields(), SM.unpack_fields_values(user=request.user)

    
    if request.method == 'POST':
        form = GradeSolutions(request.POST)
        if form.is_valid():
            SM.update(form)
        return render(request, "grade.html", {
                "query_results" : query,
                "model_headers" : header,
                'form': form})
    else:
        form = GradeSolutions()
        return render(request, "grade.html", {
                "query_results" : query,
                "model_headers" : header,
                'form': form
            })
    # Достать все решения для учителя у которых нет оценки
    # Ввести форму для оценки 

def logout_view(request):
    logout(request)
    
    return HttpResponseRedirect('/login/')