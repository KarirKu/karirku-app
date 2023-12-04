from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser
from .models import LowonganKerja
from .serializers import LowonganKerjaSerializer
from .permissions import IsOwner, IsAlumniUser

class DetailLowonganKerja(RetrieveAPIView):
    queryset = LowonganKerja.objects.all()
    serializer_class = LowonganKerjaSerializer

class LowonganKerjaViewAll(ListAPIView):
    queryset = LowonganKerja.objects.all()
    serializer_class = LowonganKerjaSerializer

class DeleteLowonganKerja(DestroyAPIView):
    permission_classes = (IsOwner|IsAdminUser,)
    queryset = LowonganKerja.objects.all()
    serializer_class = LowonganKerjaSerializer

class CreateLowonganKerja(CreateAPIView):
    permission_classes = (IsAlumniUser,)
    queryset = LowonganKerja.objects.all()
    serializer_class = LowonganKerjaSerializer

    def perform_create(self, serializer, **kwargs):
        serializer.save(alumni=self.request.user)

class EditLowonganKerja(UpdateAPIView):
    permission_classes = (IsOwner,)
    queryset = LowonganKerja.objects.all()
    serializer_class = LowonganKerjaSerializer
