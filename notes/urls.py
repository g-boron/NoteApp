from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('<int:pk>/', views.NoteDetailView.as_view(), name='show'),
    path('show_notes/', views.NotesListView.as_view(), name='show_notes'),
    path('add_note/', views.CreateNoteView.as_view(), name='add_note'),
    path('<int:pk>/delete/', views.DeleteNoteView.as_view(), name='delete'),
    path('<int:pk>/edit/', views.EditNoteView.as_view(), name='edit'),
    path('<int:pk>/stats/', views.StatsNoteView.as_view(), name='stats'),
    path('download/<int:file_id>/', views.download, name='download'),
    path('invite/<int:pk>', views.invite_user, name='invite'),
    path('show_notifications/', views.NotificationsListView.as_view(), name='show_notifications'),
    path('<int:pk>/decline_notification/', views.DeclineNotificationView.as_view(), name='decline_notification'),
    path('<int:pk>/check/', views.check, name='check'),
    path('<int:pk>/accept', views.accept_invitation, name='accept'),
    path('delete_file/<int:pk>/<int:note>', views.detele_file, name='delete_file'),
    path('<int:pk>/check_edit', views.check_edit, name='check_edit'),
    path('delete_member/<int:pk>/<str:username>', views.delete_member, name='delete_member'),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='profile'),
    path('edit_profile/<int:pk>', views.EditUserProfileView.as_view(), name='edit_profile'),
    path('<int:note_id>/add_reminder/', views.add_reminder, name='add_reminder'),
    path('reminders/', views.RemindersListView.as_view(), name='reminders'),
    path('events/', views.events, name='events'),
    path('delete_reminder/<int:pk>/<int:note_id>', views.delete_reminder, name='delete_reminder'),
    path('download_note/<int:pk>', views.download_note, name='download_note'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)