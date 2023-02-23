from django import forms
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class AddNewNote(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    note_text = forms.CharField(label='Note', widget=forms.Textarea)
    img = forms.ImageField(required=False)