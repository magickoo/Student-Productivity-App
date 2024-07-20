from django import forms
from django.db.models import fields
from django.forms import widgets
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class NoteForm(forms.ModelForm):
    class Meta:
        model= Note #mapping models
        fields = ['title','description']