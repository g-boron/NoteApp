from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:note_id>/', views.show, name='show'),
    path('show_notes/', views.show_notes, name='show_notes'),
    path('add_note/', views.add_note, name='add_note'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)