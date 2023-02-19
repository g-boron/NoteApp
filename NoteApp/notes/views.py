from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import AddNewNote
from django.utils import timezone

# Create your views here.
def index(request):

    return render(request, 'notes/index.html')


def show_notes(request):
    notes = Note.objects.all()
    context = {'notes': notes}

    return render(request, 'notes/show_notes.html', context)

def show(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    context = {'note': note}

    return render(request, 'notes/show.html', context)


def add_note(request):
    if request.method == 'POST':
        form = AddNewNote(request.POST)

        if form.is_valid():
            f_title = form.cleaned_data['title']
            f_note_text = form.cleaned_data['note_text']
            n = Note(title=f_title, note_text=f_note_text, add_date=timezone.now())
            n.save()
            return redirect('show_notes')
    else:
        form = AddNewNote()

    context = {'form': form}    

    return render(request, 'notes/add_note.html', context)
