from rest_framework import serializers
from .models import CeritaAlumni

class CeritaAlumniSerializer(serializers.ModelSerializer):
    alumni = serializers.CharField(source='alumni.id')

    class Meta:
        model = CeritaAlumni
        fields = ['id', 'judul', 'isi', 'alumni']