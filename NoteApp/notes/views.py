from django.shortcuts import render, get_object_or_404
from .models import Note

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
    pass
