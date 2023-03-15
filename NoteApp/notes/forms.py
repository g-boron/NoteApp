from django import forms
from .models import Note


class AddNewNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'note_text', 'img', 'doc', ]
