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
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('download/<int:file_id>/', views.download, name='download'),
    path('invite/<int:pk>', views.invite_user, name='invite'),
    path('show_notifications/', views.NotificationsListView.as_view(), name='show_notifications'),
    path('<int:pk>/decline_notification/', views.DeclineNotificationView.as_view(), name='decline_notification'),
    path('<int:pk>/check/', views.check, name='check'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)