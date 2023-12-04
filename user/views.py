from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from .models import User
from .serializers import UserSerializer
from .permissions import IsCurrentUserOrReadOnly, IsAlumniUser

class Register(CreateAPIView):
    queryset = User.objects.all()
    # permission_classes=[IsAlumniUser]
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = UserSerializer
    throttle_scope = 'register'

class UserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsCurrentUserOrReadOnly]
    http_method_names = ['get', 'head', 'patch']
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CurrentUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)