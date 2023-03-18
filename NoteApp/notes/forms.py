from django import forms
from .models import Note
from django.forms.widgets import ClearableFileInput


class AddNewNote(forms.ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Note
        fields = ['title', 'note_text', ]

    def __init__(self, *args, **kwargs):
        super(AddNewNote, self).__init__(*args, **kwargs)
        self.fields['file_field'].label = "Files"