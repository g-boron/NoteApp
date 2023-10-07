from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Note, NoteFile, User, Notification, Category, Reminder
from .forms import AddNewNote, InviteUser, EditProfileForm
from django.utils import timezone as dj_timezone
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from datetime import timedelta, datetime, timezone
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import os
import mimetypes
from wsgiref.util import FileWrapper
from django.contrib import messages
from collections import Counter
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


# Create your views here.
class IndexPageView(TemplateView):
    template_name = 'notes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
            context["unread_notifications"] = unread_notifications
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
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        context['notes'] = notes_page
        categories = Category.objects.all()
        context['categories'] = categories
        context['selected_category'] = self.request.GET.get('category')
        context['searched'] = self.request.GET.get('q')
        context['sort_value'] = self.request.GET.get('sortby')
        context['current_language'] = self.request.LANGUAGE_CODE
        return context

    def get_queryset(self):
        queryset = Note.objects.filter(members__contains=[self.request.user]).order_by('-add_date')
        category = self.request.GET.get('category')
        search = self.request.GET.get('q')
        sort = self.request.GET.get('sortby')
        
        if category == 'Wszystkie':
            category = 'All'
        
        if search and category and category != 'All':
            queryset = queryset.filter(Q(title__icontains=search) & Q(category__slug=category))
        elif category and category != 'All':
            queryset = queryset.filter(category__slug=category)
        elif search:
            queryset = queryset.filter(title__icontains=search)
        
        if sort == 'Najnowsze':
            sort = 'Latest'
        elif sort == 'Najstarsze':
            sort = 'Oldest'

        if sort == 'Oldest':
            queryset = queryset.order_by('add_date')
        elif sort == 'Z-a':
            queryset = queryset.order_by('-title')
        elif sort == 'A-z':
            queryset = queryset.order_by('title')
        else:
            queryset = queryset.order_by('-add_date')
        
        return queryset


class NoteDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Note
    template_name = 'notes/show.html'

    def get(self, request, *args, **kwargs):
        note = self.get_object()
        if Note.objects.filter(members__contains=[self.request.user], id=note.id):
            return super().get(request, *args, **kwargs)
        else:
            return render(request, 'notes/error.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InviteUser()
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        reminders = Reminder.objects.filter(note=self.object.id, user=self.request.user)
        context['reminders'] = reminders
        context['current_language'] = self.request.LANGUAGE_CODE
        return context


class CreateNoteView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Note
    template_name = 'notes/add_note.html'
    form_class = AddNewNote

    def get_success_url(self):
        return reverse('show', kwargs={'pk': self.object.pk})

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        return context


class DeleteNoteView(DeleteView):
    model = Note
    template_name = 'notes/show.html'
    success_url = reverse_lazy('show_notes')


class EditNoteView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Note
    template_name = 'notes/add_note.html'
    form_class = AddNewNote

    def get_success_url(self):
        return reverse('show', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        context['form'] = self.form_class(instance=self.object)
        context['files'] = self.object.notefile_set.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.edit_dates is None:
            self.object.edit_dates = []
        date = dj_timezone.now()
        correct_date = date + timedelta(hours=1) 
        self.object.edit_dates.append(correct_date.strftime("%Y-%m-%d %H:%M:%S"))
        self.object.save()

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
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        if Note.objects.filter(members__contains=[self.request.user], id=note.id):
            context['note'] = note
        
        if note.add_date.date() == datetime.now(timezone.utc).date():
            num_days = (datetime.now(timezone.utc) - note.add_date).days + 1
        else:
            num_days = (datetime.now(timezone.utc) - note.add_date).days + 2
            
        date_list = [note.add_date + timedelta(days=i) for i in range(num_days)]
        date_list = [date.date() for date in date_list]
        labels = [date.strftime('%Y-%m-%d') for date in date_list]

        edit_counts = Counter(date.date() for date in note.edit_dates)
        data = [edit_counts[date] for date in date_list]
        
        context['labels'] = labels
        context['data'] = data

        return context

    def get(self, request, *args, **kwargs):
        note = self.get_object()
        if Note.objects.filter(members__contains=[self.request.user], id=note.id):
            return super().get(request, *args, **kwargs)
        else:
            return render(request, 'notes/error.html')


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
            if User.objects.filter(username=username).exists() and username != request.user.username and not \
                    Note.objects.filter(members__contains=[username], id=note.id):
                notification = Notification(
                    message=f"Do you want to join to {User.objects.get(username=note.user)}'s note: {note.title}?",
                    message_pl=f'Czy chcesz dołączyć do notatki użytkownika {User.objects.get(username=note.user)}: {note.title}?',
                    user=User.objects.get(username=username),
                    note_id=note.id
                )
                notification.save()
                if request.LANGUAGE_CODE == 'en':
                    messages.success(request, 'Successfully invited user!')
                else:
                    messages.success(request, 'Pomyślne zaproszono użytkownika!')
            else:
                print('Error')
                if request.LANGUAGE_CODE == 'en':
                    messages.error(request, 'You cannot add this user!')
                else:
                    messages.error(request, 'Nie można dodać tego użytkownika!')

            return redirect('show', pk=note.id)

    context = {
        'form': form
    }

    return render(request, context)


class NotificationsListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Notification
    template_name = 'notes/notifications.html'

    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = self.get_queryset()
        paginator = Paginator(notifications, self.paginate_by)
        page = self.request.GET.get('page')
        notifications_page = paginator.get_page(page)
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        context['notifications'] = notifications_page
        context['current_language'] = self.request.LANGUAGE_CODE
        return context

    def get_queryset(self):
        queryset = Notification.objects.filter(user__id=self.request.user.id).order_by("-timestamp")
        return queryset


class DeclineNotificationView(DeleteView):
    model = Notification
    template_name = 'notes/notifications.html'
    success_url = reverse_lazy('show_notifications')


def check(request, pk):
    notification = get_object_or_404(Notification, pk=pk)

    if notification.is_read:
        notification.is_read = False
        notification.save()
    else:
        notification.is_read = True
        notification.save()

    return HttpResponseRedirect(reverse('show_notifications'))


def accept_invitation(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    note = get_object_or_404(Note, pk=notification.note_id)
    user = get_object_or_404(User, pk=notification.user_id)
    note.members.append(user.username)
    note.save()
    notification.delete()

    return HttpResponseRedirect(reverse('show_notes'))
    

def detele_file(request, pk, note):
    note = get_object_or_404(Note, pk=note)
    file = NoteFile.objects.get(id=pk)
    file.delete()

    return redirect('show', pk=note.id)
    

def check_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if note.allow_edits:
        note.allow_edits = False
        note.save()
    else:
        note.allow_edits = True
        note.save()

    return redirect('show', pk=note.id)


def delete_member(request, pk, username):
    note = get_object_or_404(Note, pk=pk)
    note.members.remove(username)
    note.save()

    return redirect('show', pk=note.id)


class UserProfileView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = User
    template_name = 'notes/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        other_cat = Note.objects.filter(user=self.request.user, category_id=8).count()
        private_cat = Note.objects.filter(user=self.request.user, category_id=14).count()
        work_cat = Note.objects.filter(user=self.request.user, category_id=13).count()
        school_cat = Note.objects.filter(user=self.request.user, category_id=12).count()
        shopping_cat = Note.objects.filter(user=self.request.user, category_id=9).count()
        cooking_cat = Note.objects.filter(user=self.request.user, category_id=11).count()
        travel_cat = Note.objects.filter(user=self.request.user, category_id=10).count()
        labels = ['Other', 'Private', 'Work', 'School', 'Shopping', 'Cooking', 'Travel']
        labels_pl = ['Inne', 'Prywatne', 'Praca', 'Szkoła', 'Zakupy', 'Gotowanie', 'Podróżowanie']
        data = [other_cat, private_cat, work_cat, school_cat, shopping_cat, cooking_cat, travel_cat]
        if self.request.LANGUAGE_CODE == 'en':
            context['labels'] = labels
        else:
            context['labels'] = labels_pl
        context['data'] = data
        return context


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = User
    template_name = 'notes/edit_profile.html'
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications
        context['form'] = self.form_class(instance=self.object)
        return context


def add_reminder(request, note_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        date = datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.strptime(time, '%H:%M').time()

        whole_date = datetime.combine(date, time)

        note = Note.objects.get(pk=note_id)
        reminder = Reminder.objects.create(title=title, remind_date=whole_date, note=note, user=request.user)
        if request.LANGUAGE_CODE == 'en':
            messages.success(request, 'Successfully added reminder!')
        else:
            messages.success(request, 'Pomyślnie dodano przypomnienie!')
        
        return redirect('show', pk=note_id)


class RemindersListView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'notes/reminders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False).count()
        context["unread_notifications"] = unread_notifications

        return context


def events(request):
    reminders = Reminder.objects.filter(user=request.user)

    events_list = []
    for reminder in reminders:
        reminder.remind_date += timedelta(hours=2)
        end_date = reminder.remind_date.replace(hour=23, minute=59, second=59)
        data = {
            'title': reminder.title,
            'start': reminder.remind_date.isoformat(),
            'end': end_date.isoformat(),
            'url': reverse('show', args=[reminder.note.id]),
        }
        events_list.append(data)

    return JsonResponse(events_list, safe=False, encoder=DjangoJSONEncoder)


def delete_reminder(request, pk, note_id):
    note = get_object_or_404(Note, pk=note_id)
    reminder = get_object_or_404(Reminder, pk=pk)
    reminder.delete()

    return redirect('show', pk=note.id)
