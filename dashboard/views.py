from django.core.checks import messages
from django.shortcuts import redirect, render
from . forms import DashboardForm, HomeworkForm, NoteForm, TodoForm, CreateUserForm
from . models import Note, Homework, Todo
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

def Notes(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = Note(user=request.user,title=request.POST['title'],description=request.POST['description'])
            note.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully!")
    else:
        form= NoteForm()
    note = Note.objects.filter(user=request.user)
    context = {
        'note': note ,
        'form': form
    }
    return render(request,'dashboard/notes.html',context)
    
@login_required
def delete_note(request,pk=None):
    Note.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Note
    
@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
                
            )
            homeworks.save()
            messages.success(request,f"Homework Added from {request.user.username} Successfully!")
    else:     
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context ={
        'homeworks' : homework,
        'homework_done' : homework_done,
        'form' : form
    }
    return render(request,'dashboard/homework.html',context)

@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True :
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")
