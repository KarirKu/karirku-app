from django.contrib import admin
from .models import User, Alumni, Mahasiswa, Pendidikan, PengalamanKerja, Pengalaman, Lomba

# Register your models here.
admin.site.register(User)
admin.site.register(Pendidikan)
admin.site.register(PengalamanKerja)
admin.site.register(Pengalaman)
admin.site.register(Lomba)