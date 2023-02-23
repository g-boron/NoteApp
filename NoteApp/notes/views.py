from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import AddNewNote
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    return render(request, 'notes/index.html')


@login_required(login_url='/login/')
def show_notes(request):
    notes = Note.objects.all()
    context = {'notes': notes}

    return render(request, 'notes/show_notes.html', context)


@login_required(login_url='/login/')
def show(request, note_id):
    n = Note.objects.get(user=request.user)

    note = get_object_or_404(Note, pk=note_id)

    if note.user == n.user:
        context = {'note': note}
        return render(request, 'notes/show.html', context)
    else:
        return render(request, 'notes/error.html', {})


@login_required(login_url='/login/')
def add_note(request):
    if request.method == 'POST':
        form = AddNewNote(request.POST)

        if form.is_valid():
            f_title = form.cleaned_data['title']
            f_note_text = form.cleaned_data['note_text']
            n = Note(title=f_title, note_text=f_note_text, add_date=timezone.now())
            n.save()
            request.user.note.add(n)
            return redirect('show_notes')
    else:
        form = AddNewNote()

    context = {'form': form}    

    return render(request, 'notes/add_note.html', context)
