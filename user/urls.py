from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from . import views

urlpatterns = [
    path('register', views.Register.as_view(), name='user-register'),
    path('login', TokenObtainPairView.as_view(), name='user-login'),
    path('refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('<uuid:pk>', views.UserView.as_view(), name='user-detail'),
    path('', views.CurrentUser.as_view(), name='current-user-detail'),
]