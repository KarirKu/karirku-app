from django.urls import path
from . import views

urlpatterns = [
    path('', views.now, name='current-time'),
    path('all/', views.CeritaAlumiViewAll.as_view(), name='cerita-alumni-all'),
    path('delete/<uuid:pk>/', views.DeleteCeritaAlumi.as_view(), name='delete-cerita-alumni'),
    path('detail/<uuid:pk>/', views.DetailCeritaAlumni.as_view(), name='detail-cerita-alumni'),
    path('edit/<uuid:pk>/', views.EditCeritaAlumi.as_view(), name='edit-cerita-alumni'),
    path('new/', views.NewCeritaAlumi.as_view(), name='create-cerita-alumni'),
]