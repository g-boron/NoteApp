from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import AddNewNote
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
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


class CreateNoteView(CreateView):
    model = Note
    template_name = 'notes/add_note.html'
    form_class = AddNewNote
    success_url = reverse_lazy('show_notes')

    def form_valid(self, form):
        form.instance.add_date = timezone.now()
        form.instance.user = self.request.user
        return super(CreateNote, self).form_valid(form)


class DeleteNoteView(DeleteView):
    model = Note
    template_name = 'notes/show.html'
    success_url = reverse_lazy('show_notes')


class EditNoteView(UpdateView):
    model = Note
    template_name = 'notes/add_note.html'
    form_class = AddNewNote
    success_url = reverse_lazy('show_notes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context