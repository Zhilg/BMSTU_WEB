from django.urls import path

from .views import views

urlpatterns = [
    path("", views.index, name="index"),
    path("view/", views.view, name="view"),
    path("view/check", views.check, name="check"),
    path("view/create_taskpacks", views.create_taskpacks, name="create_taskpacks"),
    path("view/show_taskpacks", views.show_taskpacks, name="show_taskpacks"),
    path("view/show_solutions", views.show_solutions, name="show_solutions"),
    
    path("view/upload_tasks", views.upload_tasks, name="upload_tasks"),
    path("view/upload_solutions", views.upload_solutions, name="upload_solutions"),
    path("view/grade_solutions", views.grade_solutions, name="grade_solutions"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('view/change_password/', views.change_password, name='change_password'),
    
    path('logout/', views.logout_view, name='logout_view')
]
