from django import forms
from .models import Project, Profile, Rate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','second_name','phone', 'bio','profile_pic']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','project_pic','description','project_link']

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        exclude = ['user', 'project']        