from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('notes/create/', views.note_create_view, name='note_create'),
    path('notes/<int:pk>/edit/', views.note_update_view, name='note_update'),
    path('notes/<int:pk>/delete/', views.note_delete_view, name='note_delete'),
]