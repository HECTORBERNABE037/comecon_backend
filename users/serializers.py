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
    
    # CAMBIO 1: Hacemos que 'name' sea de escritura para recibirlo del frontend
    # Lo usamos como CharField de escritura, pero en lectura (to_representation)
    # usaremos la lógica de unir first_name + last_name si quisieras.
    # Para simplificar y que funcione con tu frontend actual:
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
        
        # CORRECCIÓN PRINCIPAL: Eliminamos "username=..."
        # El modelo tiene username=None, así que no debemos pasarlo.
        user = User.objects.create_user(
            first_name=name, # Guardamos el nombre aquí
            **validated_data
        )
        return user
        
    # Opcional: Si quieres devolver el campo 'name' al leer el usuario
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Reconstruimos 'name' basado en lo que guardamos
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