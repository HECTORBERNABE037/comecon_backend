from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'last_four', 'holder_name', 'expiry_date', 'type']
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'nickname', 'role', 'phone', 
            'gender', 'country', 'address', 'image', 
            'allow_notifications', 'allow_camera', 'cards', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Encriptar contraseña al crear usuario
        user = User.objects.create_user(**validated_data, username=validated_data['email'])
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciales incorrectas")