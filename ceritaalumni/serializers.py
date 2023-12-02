from rest_framework import serializers
from .models import CeritaAlumni
from user.models import Alumni

class CeritaAlumniSerializer(serializers.ModelSerializer):
    alumni = serializers.PrimaryKeyRelatedField( read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = CeritaAlumni
        fields = ['id', 'judul', 'isi', 'alumni']
    
    def create(self, validated_data):
        validated_data['alumni'] = Alumni.objects.get(id=validated_data['alumni'].id)
        return CeritaAlumni.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.judul = validated_data['judul']
        instance.isi = validated_data['isi']
        instance.save()
        return instance