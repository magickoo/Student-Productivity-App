from django.core.checks import messages
from django.shortcuts import redirect, render
from . forms import NoteForm
from . models import Note 
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