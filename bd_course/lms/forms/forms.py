from django import forms

class MyUserCreationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()
    group = forms.CharField()
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    
class CreateTaskPacks(forms.Form):
    group = forms.CharField()
    N = forms.IntegerField()
    theme = forms.CharField()
    duetime = forms.DateField()

class UploadTask(forms.Form):
    filename = forms.CharField()
    theme = forms.CharField()
    
class UploadSolutions(forms.Form):
    filename = forms.CharField()
    taskpackid = forms.IntegerField()
    
class GradeSolutions(forms.Form):
    solutionid = forms.IntegerField()
    grade = forms.IntegerField()
    