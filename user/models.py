import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError('Email cannot be empty')

        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **other_fields):
        user = self.create_user(email, password=password, **other_fields)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    npm = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    nama_lengkap = models.CharField(max_length=100)
    nomor_hp = models.CharField(max_length=15)
    foto_profil = models.URLField(blank=True)
    pendidikan = models.ManyToManyField('Pendidikan', related_name='pendidikan_users')
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nama_lengkap', 'npm', 'nomor_hp']

    def __str__(self):
        return self.nama_lengkap

class Alumni(User):
    pengalaman_kerja = models.ManyToManyField('PengalamanKerja', related_name='alumni')

class Mahasiswa(User):
    pengalaman = models.ManyToManyField('Pengalaman', related_name='pengalaman_mhs')
    lomba = models.ManyToManyField('Lomba', related_name='lomba_mhs')

class Pendidikan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_perguruan_tinggi = models.CharField(max_length=100)
    prodi = models.CharField(max_length=100)
    bidang = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nama_perguruan_tinggi} - {self.prodi}"

class Pengalaman(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_pengalaman = models.CharField(max_length=100)
    nama_instansi = models.CharField(max_length=100)
    tanggal_mulai = models.DateTimeField()
    tanggal_akhir = models.DateTimeField()

class Lomba(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_lomba = models.CharField(max_length=100)
    penyelenggara = models.CharField(max_length=100)
    hasil_lomba = models.CharField(max_length=100)

class PengalamanKerja(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_pengalaman = models.CharField(max_length=100)
    nama_instansi = models.CharField(max_length=100)
    tanggal_mulai = models.DateTimeField()
    tanggal_akhir = models.DateTimeField()
