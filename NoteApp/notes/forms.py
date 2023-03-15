from django import forms
from .models import Note


class AddNewNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'note_text', 'img', 'doc', ]

    def __init__(self, *args, **kwargs):
        super(AddNewNote, self).__init__(*args, **kwargs)
        self.fields['img'].label = "Image"
        self.fields['doc'].label = "File"