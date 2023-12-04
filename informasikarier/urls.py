from django.urls import path
from . import views

urlpatterns = [
    path('', views.now, name='current-time'),
    path('all/', views.ViewAllKarier.as_view(), name='karier-all'),
    path('delete/<uuid:pk>/', views.DeleteKarier.as_view(), name='delete-karier'),
    path('detail/<uuid:pk>/', views.DetailKarier.as_view(), name='detail-karier'),
    path('edit/<uuid:pk>/', views.EditKarier.as_view(), name='edit-karier'),
    path('new/', views.NewKarier.as_view(), name='create-karier'),
]