from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Note, NoteFile, User
from .forms import AddNewNote, InviteUser
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
from django.http import HttpResponse
import os
import mimetypes
from wsgiref.util import FileWrapper



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
        queryset = Note.objects.filter(members__contains = [self.request.user])
        return queryset


class NoteDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Note
    template_name = 'notes/show.html'

    def get(self, request, *args, **kwargs):
        note = self.get_object()
        if Note.objects.filter(members__contains = [self.request.user], id=note.id):
            return super().get(request, *args, **kwargs)
        else:
            return render(request, 'notes/error.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InviteUser()
        return context


class CreateNoteView(CreateView):
    model = Note
    template_name = 'notes/add_note.html'
    form_class = AddNewNote

    def get_success_url(self):
        return reverse('show', kwargs={'pk' : self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.members is None:
            form.instance.members = [self.request.user]
        form.save(commit=False)
        
        form.instance.save()

        form_files = self.request.FILES.getlist('file_field')
        if form_files:
            for f in form_files:
                note_file = NoteFile(note=form.instance)
                note_file.file.save(f.name, f)
                note_file.save()
        

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
        context['files'] = self.object.notefile_set.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.edit_dates is None:
            self.object.edit_dates = []
        date = timezone.now()
        correct_date = date + timedelta(hours=1) 
        self.object.edit_dates.append(correct_date.strftime("%Y-%m-%d %H:%M:%S"))
        self.object.save()

        self.object.notefile_set.all().delete()

        form_files = self.request.FILES.getlist('file_field')
        if form_files:
            for f in form_files:
                note_file = NoteFile(note=form.instance)
                note_file.file.save(f.name, f)
                note_file.save()
                
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


def download(request, file_id):
    note_file = get_object_or_404(NoteFile, id=file_id)
    file_path = note_file.file.path
    file_name = note_file.file.name
    file_wrapper = FileWrapper(open(file_path, 'rb'))
    content_type = mimetypes.guess_type(file_path)[0]
    response = HttpResponse(file_wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response


def invite_user(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = InviteUser()

    if request.method == 'POST':
        form = InviteUser(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists() and username != request.user.username and not Note.objects.filter(members__contains = [username], id=note.id):
                note.members.append(username)
                note.save()
            else:
                print('Error')

            return redirect('show', pk=note.id)

    context = {
        'form': form
    }

    return render(request, context)