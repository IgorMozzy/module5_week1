from django.urls import path

from notes.views import home_view, NoteDetailView, NoteCreateView, NoteUpdateView, NoteDeleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('notes/', home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('notes/new/', NoteCreateView.as_view(), name='note_create'),
    path('notes/<int:pk>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
]
