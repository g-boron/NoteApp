from django.shortcuts import render, get_object_or_404
from .models import Note

# Create your views here.
def index(request):
    notes = Note.objects.all()
    context = {'notes': notes}

    return render(request, 'notes/index.html', context)


def show(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    context = {'note': note}

    return render(request, 'notes/show.html', context)