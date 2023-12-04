from django.http import HttpResponse
import datetime
from .models import CeritaAlumni
from .serializers import CeritaAlumniSerializer
from rest_framework.generics import ListAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from user.permissions import IsAlumniUser

def now(request):
    now = datetime.datetime.now() 
    msg = f'Today is {now}'
    return HttpResponse(msg, content_type='text/plain')

# Membaca cerita alumni
class DetailCeritaAlumni(RetrieveAPIView):
    queryset = CeritaAlumni.objects.all()
    serializer_class = CeritaAlumniSerializer

# Ambil seluruh cerita alumni yang ada
class CeritaAlumiViewAll(ListAPIView):
    queryset = CeritaAlumni.objects.all()
    serializer_class = CeritaAlumniSerializer

# Hapus cerita alumni jika merupakan owner atau admin
class DeleteCeritaAlumi(DestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly|IsAdminUser,)

    queryset = CeritaAlumni.objects.all()
    serializer_class = CeritaAlumniSerializer

# Buat cerita alumni jika authenticated dan alumni
class NewCeritaAlumi(CreateAPIView):
    permission_classes = (IsAuthenticated&IsAlumniUser,)

    queryset = CeritaAlumni.objects.all()
    serializer_class = CeritaAlumniSerializer

    def perform_create(self, serializer, **kwargs):
        serializer.save(alumni=self.request.user)

# Buat sunting cerita alumni
class EditCeritaAlumi(UpdateAPIView):
    permission_classes = (IsAuthenticated&IsOwnerOrReadOnly,)

    queryset = CeritaAlumni.objects.all()
    serializer_class = CeritaAlumniSerializer