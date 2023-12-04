from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
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
        ret = super().to_representation(instance)
        return ret