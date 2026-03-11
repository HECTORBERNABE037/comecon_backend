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
    name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'nickname', 'role', 'phone', 
            'gender', 'country', 'address', 'image', 
            'allow_notifications', 'allow_camera', 'cards', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extraemos 'name' si viene del frontend para guardarlo en first_name
        name = validated_data.pop('name', '')
        user = User.objects.create_user(
            first_name=name, # Guardamos el nombre aquí
            **validated_data
        )
        return user
    
    def update(self, instance, validated_data): # CORRECION DEL BUG DE ACTUALIZACION DEL NOMBRE DEL PERFIL
        name = validated_data.pop('name', None)
        if name is not None:
            instance.first_name = name
            
        # Llamamos al método update original para que guarde el resto de los campos
        return super().update(instance, validated_data)
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Reconstruimos 'name' basado en lo guardado
        ret['name'] = instance.first_name
        return ret

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciales incorrectas")