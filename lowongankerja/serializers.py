from rest_framework import serializers
from .models import LowonganKerja
from informasikarier.models import Karier
from user.models import User

class LowonganKerjaSerializer(serializers.ModelSerializer):
    alumni = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    karier = serializers.PrimaryKeyRelatedField(queryset=Karier.objects.all())

    class Meta:
        model = LowonganKerja
        fields = ['id', 'posisi', 'nama_instansi', 'deskripsi', 'eligibilitas', 'tanggal_buka', 'tanggal_tutup', 'link', 'alumni', 'karier']
    
    def create(self, validated_data):
        validated_data['alumni'] = User.objects.get(id=validated_data['alumni'].id)
        return LowonganKerja.objects.create(**validated_data)

    def update(self, instance: LowonganKerja, validated_data):
        return instance.set_details(
            posisi=validated_data['posisi'],
            nama_instansi=validated_data['nama_instansi'],
            deskripsi=validated_data['deskripsi'],
            eligibilitas=validated_data['eligibilitas'],
            tanggal_buka=validated_data['tanggal_buka'],
            tanggal_tutup=validated_data['tanggal_tutup'],
            link=validated_data['link'],
            karier=Karier.objects.get(nama=validated_data['karier'])
        )
    