from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:note_id>/', views.show, name='show'),
    path('show_notes/', views.show_notes, name='show_notes'),
    path('add_note/', views.add_note, name='add_note'),
    path('<int:note_id>/delete/', views.delete, name='delete'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)