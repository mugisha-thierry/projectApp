from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import SignUpForm,ProjectForm,UpdateUserProfileForm,RateForm
from .email import send_welcome_email
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Profile,Project,Rate
from django.contrib.auth.models import User
from .serializer import ProfileSerializer,ProjectSerializer
from django.urls import reverse

class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)            

def home(request):
    projects = Project.objects.all()
    rates = Rate.objects.all()
    users = User.objects.exclude(id=request.user.id)
    form = ProjectForm(request.POST or None, files=request.FILES)      
    if form.is_valid():
        project=form.save(commit=False)
        project.user = request.user.profile
        project.save()
        return redirect('home')
    context = {
        'projects': projects,
        'form': form,
        'users':users,
        'rates':rates,
    }
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            form.save()
            send_welcome_email(name,email)
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, 'register/register.html', {'form': form})
   

def search_project(request):
    rates = Rate.objects.all()
    if 'searchproject' in request.GET and request.GET["searchproject"]:
        search_term = request.GET.get("searchproject")
        searched_project = Project.search_by_title(search_term)
        message = f"{search_term}"
        context = {'projects':searched_project,'message': message}

        return render(request, "search.html",context)
    else:
      message = "You haven't searched for any term"
      return render(request, 'search.html',{"message":message})   


def profile(request, username):
    projects = request.user.profile.projects.all()
    if request.method == 'POST':
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProjectForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user.profile
            project.save()
    else:
        form = ProjectForm()

    context = {
        'prof_form': prof_form,
        'projects': projects,
        'form':form,

    }
    return render(request, 'profile.html', context)

def project(request,id):
    project = Project.objects.get(id = id)
    rates = Rate.objects.order_by('-date')
    current_user = request.user
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']
            rate = Rate()
            rate.project = project
            rate.user = current_user
            rate.design = design
            rate.usability = usability
            rate.content = content
            rate.average = (rate.design + rate.usability + rate.content)/3
            rate.save()
            return HttpResponseRedirect(reverse('project', args=(project.id,)))
    else:
        form = RateForm()
    context={"project":project,"rates":rates,"form":form}
    return render(request, 'project.html',context)    