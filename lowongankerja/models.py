from django.db import models
import uuid

from user.models import User
from informasikarier.models import Karier

class LowonganKerja(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    posisi = models.CharField(max_length=64, null=False)
    nama_instansi = models.CharField(max_length=64, null=False)
    deskripsi = models.TextField(null=False)
    eligibilitas = models.TextField(null=False)
    tanggal_buka = models.DateTimeField(null=False)
    tanggal_tutup = models.DateTimeField(null=True)
    link = models.URLField()
    alumni = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    karier = models.ForeignKey(Karier, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f'{self.posisi} - {self.nama_instansi}'
    
    def lihat_lowongan_kerja():
        return LowonganKerja.objects.all()
    
    def set_details(self, posisi, nama_instansi, deskripsi, eligibilitas, tanggal_buka, tanggal_tutup, link, karier):
        if tanggal_tutup is not None and tanggal_buka > tanggal_tutup:
            raise Exception('Tanggal tutup harus setelah tanggal buka')
        self.posisi = posisi
        self.nama_instansi = nama_instansi
        self.deskripsi = deskripsi
        self.eligibilitas = eligibilitas
        self.tanggal_buka = tanggal_buka
        self.tanggal_tutup = tanggal_tutup
        self.link = link
        self.karier = karier
        self.save()
        return self
