from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import AddNewNote
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class IndexPageView(TemplateView):
    template_name = 'notes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['last_note'] = Note.objects.filter(user=self.request.user).last()
        else:
            context['last_note'] = None

        return context
  

class NotesListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Note
    template_name = 'notes/show_notes.html'


class NoteDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Note
    template_name = 'notes/show.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        note = self.get_object()
        if note.user == self.request.user:
            context['note'] = note

        return context

    def get(self, request, *args, **kwargs):
        note = self.get_object()
        if note.user == self.request.user:
            return super().get(request, *args, **kwargs)
        else:
            return render(request, 'notes/error.html')


@login_required(login_url='/login/')
def add_note(request):
    if request.method == 'POST':
        form = AddNewNote(request.POST, request.FILES)

        if form.is_valid():
            f_title = form.cleaned_data['title']
            f_note_text = form.cleaned_data['note_text']
            f_img = form.cleaned_data['img']
            n = Note(title=f_title, note_text=f_note_text, add_date=timezone.now(), img=f_img)
            n.save()
            request.user.note.add(n)
            return redirect('show_notes')
    else:
        form = AddNewNote()

    context = {'form': form}    

    return render(request, 'notes/add_note.html', context)


def delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()

    return redirect('show_notes')