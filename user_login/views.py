from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import get_language


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            if get_language() == 'en':
                subject = 'NoteApp account has been created.'
                message = f'Hi {form.instance.username}!\n\nThank you for creating an account in our app. Welcome in NoteApp community!\n\nBest regards,\nNoteApp Team.'
            elif get_language() == 'pl':
                subject = 'Konto NoteApp zostało założone.'
                message = f'Cześć {form.instance.username}!\n\nDziękujemy za założenie konta w naszej aplikacji. Witaj w społeczności NoteApp!\n\nPozdrowienia,\nZespół NoteApp.'
            
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form.instance.email, ]
            send_mail( subject, message, email_from, recipient_list )
        return redirect('/')
    else:
        form = RegisterForm()

    context = {'form': form}

    return render(request, 'user_login/register.html', context)