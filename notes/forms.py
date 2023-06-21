from django import forms
from .models import Note, User
from django.forms.widgets import ClearableFileInput


class AddNewNote(forms.ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Note
        fields = ['title', 'note_text', 'category', ]

    def __init__(self, *args, **kwargs):
        super(AddNewNote, self).__init__(*args, **kwargs)
        self.fields['file_field'].label = "Files"


class InviteUser(forms.ModelForm):
    username = forms.CharField(max_length=200)

    class Meta:
        model = Note
        fields = ['username',]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]