from django.core.checks import messages
from django.shortcuts import redirect, render
#from . forms import CreateUserForm
#from . models import Homework, Note, Todo
from django.contrib import messages
from django.views import generic
#from youtubesearchpython import VideosSearch
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
# Create your views here.

@login_required
def home(request):
    return render(request,'partials/home.html')

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/register.html'
    
    def form_valid(self, form):
        view = super(SignUp,self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view