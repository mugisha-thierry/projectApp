from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .email import send_welcome_email
# Create your views here.
def home(request):
    return render(request,'home.html')

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