from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import User, Alumni, Mahasiswa, PengalamanKerja, Pengalaman, Lomba, Pendidikan
from django.contrib.auth.hashers import make_password

class PendidikanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pendidikan
        fields = ('id', 'nama_perguruan_tinggi', 'prodi', 'bidang')
        
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

class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )    
    pendidikan = PendidikanSerializer(many=True)
    pengalaman_kerja = PengalamanKerjaSerializer(many=True)
    pengalaman = PengalamanSerializer(many=True)
    lomba = LombaSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'nama_lengkap', 'npm', 'nomor_hp', 'foto_profil', 'pendidikan', 'user_type', 'pengalaman_kerja', 'pengalaman', 'lomba']
        extra_kwargs = {
            'pengalaman_kerja': {'required': False, 'allow_null': True},
            'pengalaman': {'required': False, 'allow_null': True},
            'lomba': {'required': False, 'allow_null': True}
        }

    def validate(self, attrs):
        user_type = attrs.get('user_type')

        if user_type == 'alumni' and 'pengalaman_kerja' not in attrs:
            raise serializers.ValidationError(
                "Pengalaman Kerja is required for Alumni."
            )
        elif user_type == 'mahasiswa' and ('pengalaman' not in attrs or 'lomba' not in attrs):
            raise serializers.ValidationError(
                "Pengalaman and Lomba are required for Mahasiswa."
            )

        return attrs
    
    def create(self, validated_data):
        pendidikan_data = validated_data.pop('pendidikan')
        validated_data['password'] = make_password(validated_data['password'])
       
        excluded_fields = ['pengalaman', 'pengalaman_kerja', 'lomba']
        filtered_data = {key: value for key, value in validated_data.items() if key not in excluded_fields}

        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(filtered_data)

        for pendidikan_item in pendidikan_data:
            Pendidikan.objects.create(user=user, **pendidikan_item)

        user_type = validated_data.pop('user_type')
        if user_type == 'alumni':
            pengalaman_kerja_data = validated_data.pop('pengalaman_kerja')
            alumni = Alumni.objects.create(user_ptr=user, user=user)
            
            # Assign pengalaman_kerja to Alumni
            for kerja_item in pengalaman_kerja_data:
                PengalamanKerja.objects.create(user=user, **kerja_item)
                alumni.pengalaman_kerja.add(kerja_item)
            
        elif user_type == 'mahasiswa':
            pengalaman_data = validated_data.pop('pengalaman')
            lomba_data = validated_data.pop('lomba')

            mahasiswa = Mahasiswa.objects.create(user_ptr=user, user=user)

            # Create Pengalaman and Lomba instances for Mahasiswa
            for pengalaman_item in pengalaman_data:
                Pengalaman.objects.create(user=user, **pengalaman_item)
            for lomba_item in lomba_data:
                Lomba.objects.create(user=user, **lomba_item)

            mahasiswa.lomba.set(lomba_data)
            mahasiswa.pengalaman.set(pengalaman_data)
        
        return user

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate_email(self, value):
        if self.instance and value != self.instance.email:
            raise serializers.ValidationError('email is immutable once set.')
        return value

    def validate_npm(self, value):
        if self.instance and value != self.instance.npm:
            raise serializers.ValidationError('npm is immutable once set.')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        pendidikan_data = Pendidikan.objects.filter(user=instance.id)
        representation['pendidikan'] = PendidikanSerializer(pendidikan_data, many=True).data
        return representation

    def update(self, instance, validated_data):
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