from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import User, Alumni, Mahasiswa, PengalamanKerja, Pengalaman, Lomba

class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'nama_lengkap', 'npm', 'nomor_hp', 'foto_profil']

    def create(self, validated_data):
        user_type = validated_data.pop('user_type', None)
        user = super().create(validated_data)
        user.set_password(validated_data['password'])

        if user_type == 'alumni':
            Alumni.objects.create(user=user, **validated_data)
        elif user_type == 'mahasiswa':
            Mahasiswa.objects.create(user=user, **validated_data)

        return user

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate_email(self, value):
        if self.instance and value != self.instance.email:
            raise serializers.ValidationError('email is immutable once set.')
        return value

    def to_representation(self, instance):
        """ Custom representation based on user type """
        rep = super(UserSerializer, self).to_representation(instance)
        if hasattr(instance, 'alumni'):
            # Fetch PengalamanKerja related to this alumni
            pengalaman_kerja = instance.alumni.pengalaman_kerja.all()
            rep['pengalaman_kerja'] = PengalamanKerjaSerializer(pengalaman_kerja, many=True).data
        elif hasattr(instance, 'mahasiswa'):
            # Fetch Pengalaman and Lomba related to this mahasiswa
            pengalaman = instance.mahasiswa.pengalaman.all()
            lomba = instance.mahasiswa.lomba.all()
            rep['pengalaman'] = PengalamanSerializer(pengalaman, many=True).data
            rep['lomba'] = LombaSerializer(lomba, many=True).data

        return rep

    def update(self, instance, validated_data):
        """ Custom update method to handle different user types """
        if hasattr(instance, 'alumni'):
            alumni_data = {k: v for k, v in validated_data.items() if k in AlumniSerializer.Meta.fields}
            for attr, value in alumni_data.items():
                setattr(instance.alumni, attr, value)
            instance.alumni.save()
        elif hasattr(instance, 'mahasiswa'):
            mahasiswa_data = {k: v for k, v in validated_data.items() if k in MahasiswaSerializer.Meta.fields}
            for attr, value in mahasiswa_data.items():
                setattr(instance.mahasiswa, attr, value)
            instance.mahasiswa.save()
        return super(UserSerializer, self).update(instance, validated_data)
    
class AlumniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumni
        fields = '__all__'

class MahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = '__all__'
    
class PengalamanKerjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PengalamanKerja
        fields = ['id', 'nama_pengalaman', 'nama_instansi', 'tanggal_mulai', 'tanggal_akhir']

class PengalamanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengalaman
        fields = ['id', 'nama_pengalaman', 'nama_instansi', 'tanggal_mulai', 'tanggal_akhir']

class LombaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lomba
        fields = ['id', 'nama_lomba', 'penyelenggara', 'hasil_lomba']
