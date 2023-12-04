import uuid
from django.db import models
from user.models import User

class Karier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    deskripsi_pekerjaan = models.TextField()
    kompetensi = models.CharField(max_length=255)
    tanggung_jawab = models.CharField(max_length=255)

    def __str__(self):
        return self.nama