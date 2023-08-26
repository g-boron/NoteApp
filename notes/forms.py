from django import forms
from .models import Note, User


class AddNewNote(forms.ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'multiple': True, 'style': 'font-size: 22px;'}
    ), required=False)

    class Meta:
        model = Note
        fields = ['title', 'note_text', 'category', ]
        widgets = {
            'category': forms.Select(attrs={'style': 'font-size: 22px;'}),
            'title': forms.TextInput(attrs={'style': 'font-size: 22px;'}),
            'note_text': forms.Textarea(attrs={'style': 'font-size: 22px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddNewNote, self).__init__(*args, **kwargs)
        self.fields['file_field'].label = "Files"


class InviteUser(forms.ModelForm):
    username = forms.CharField(max_length=200)

    class Meta:
        model = Note
        fields = ['username', ]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]
        widgets = {
            'first_name': forms.TextInput(attrs={'style': 'font-size: 22px;'}),
            'last_name': forms.TextInput(attrs={'style': 'font-size: 22px;'}),
            'email': forms.EmailInput(attrs={'style': 'font-size: 22px;'}),
        }
