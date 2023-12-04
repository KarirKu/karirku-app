from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.LowonganKerjaViewAll.as_view(), name='lowongan-kerja-all'),
    path('delete/<uuid:pk>/', views.DeleteLowonganKerja.as_view(), name='delete-lowongan-kerja'),
    path('detail/<uuid:pk>/', views.DetailLowonganKerja.as_view(), name='detail-lowongan-kerja'),
    path('edit/<uuid:pk>/', views.EditLowonganKerja.as_view(), name='edit-lowongan-kerja'),
    path('new/', views.CreateLowonganKerja.as_view(), name='create-lowongan-kerja'),
]