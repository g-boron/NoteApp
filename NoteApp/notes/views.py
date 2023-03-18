from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Note
from .forms import AddNewNote
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from datetime import timedelta
from django.db.models import Q
from django.http import HttpResponse, Http404


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

    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notes = self.get_queryset()
        paginator = Paginator(notes, self.paginate_by)
        page = self.request.GET.get('page')
        notes_page = paginator.get_page(page)
        context['notes'] = notes_page
        return context

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)
        return queryset


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

    def get_success_url(self):
        return reverse('show', kwargs={'pk' : self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user

        form_files = self.request.FILES.getlist('file_field')
        if form_files:
            for f in form_files:
                form.instance.files.append(f)

        return super(CreateNoteView, self).form_valid(form)


class DeleteNoteView(DeleteView):
    model = Note
    template_name = 'notes/show.html'
    success_url = reverse_lazy('show_notes')


class EditNoteView(UpdateView):
    model = Note
    template_name = 'notes/add_note.html'
    form_class = AddNewNote

    def get_success_url(self):
        return reverse('show', kwargs={'pk' : self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.edit_dates is None:
            self.object.edit_dates = []
        date = timezone.now()
        correct_date = date + timedelta(hours=1) 
        self.object.edit_dates.append(correct_date.strftime("%Y-%m-%d %H:%M:%S"))
        self.object.save()
        return super().form_valid(form)


class StatsNoteView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Note
    template_name = 'notes/stats.html'

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

class SearchResultsView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Note
    template_name = 'notes/search_results.html'

    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notes = self.get_queryset()
        paginator = Paginator(notes, self.paginate_by)
        page = self.request.GET.get('page')
        notes_page = paginator.get_page(page)
        context['notes'] = notes_page
        context['query'] = self.request.GET.get('q')
        return context

    
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Note.objects.filter(
            Q(title__icontains=query) & Q(user=self.request.user)
        )
        return object_list
