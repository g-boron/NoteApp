from django import forms


class AddNewNote(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    note_text = forms.CharField(label='Note', widget=forms.Textarea)