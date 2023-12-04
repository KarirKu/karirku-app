from django.http import HttpResponse
import datetime
from .models import Karier
from .serializers import KarierSerializer
from rest_framework.generics import ListAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

def now(request):
    now = datetime.datetime.now() 
    msg = f'Now is {now}'
    return HttpResponse(msg, content_type='text/plain')

# Melihat daftar karier yang tersedia
class ViewAllKarier(ListAPIView):
    queryset = Karier.objects.all()
    serializer_class = KarierSerializer

# Melihat detail karier
class DetailKarier(RetrieveAPIView):
    queryset = Karier.objects.all()
    serializer_class = KarierSerializer

# Hapus karier jika user merupakan admin
class DeleteKarier(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Karier.objects.all()
    serializer_class = KarierSerializer

# Buat informasi karier jika user adalah admin
class NewKarier(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Karier.objects.all()
    serializer_class = KarierSerializer

    def perform_create(self, serializer, **kwargs):
        serializer.save(admin=self.request.user)

# Sunting informasi karier jika user merupakan admin
class EditKarier(UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Karier.objects.all()
    serializer_class = KarierSerializer