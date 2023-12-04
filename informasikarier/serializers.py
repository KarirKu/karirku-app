from rest_framework import serializers
from .models import Karier
from user.models import User

class KarierSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Karier
        fields = ['id', 'admin', 'nama', 'deskripsi_pekerjaan', 'kompetensi', 'tanggung_jawab']
    
    def create(self, data):
        data['admin'] = User.objects.get(id=data['admin'].id, is_staff=True)
        return Karier.objects.create(**data)

    def update(self, instance, data):
        instance.nama = data['nama']
        instance.deskripsi_pekerjaan = data['deskripsi_pekerjaan']
        instance.kompetensi = data['kompetensi']
        instance.tanggung_jawab = data['tanggung_jawab']
        instance.save()
        return instance