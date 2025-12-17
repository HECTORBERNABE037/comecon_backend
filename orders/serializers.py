from rest_framework import serializers
from .models import Order, OrderItem, Cart
from catalog.serializers import ProductSerializer
from catalog.models import Product

class CartSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', 'product_details']
        extra_kwargs = {'product': {'write_only': True}}

class OrderItemSerializer(serializers.ModelSerializer):
    # Usamos PrimaryKeyRelatedField para escritura (recibir ID) y lectura (ver ID)
    # Si quieres ver detalles del producto al leer, usa SerializerMethodField o nested serializer en lectura.
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        source='product', # Mapea 'product_id' del JSON al campo 'product' del modelo
        write_only=True
    )
    product_details = serializers.StringRelatedField(source='product', read_only=True) # Para ver info al leer

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_details', 'quantity', 'price_at_moment']

class OrderSerializer(serializers.ModelSerializer):
    # Permitimos escribir items anidados
    items = OrderItemSerializer(many=True)
    
    # User será readonly porque lo tomaremos del request
    user = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'status', 'date', 'delivery_time', 'history_notes', 'items', 'payment_method', 'address']
        read_only_fields = ['status', 'date']

    def create(self, validated_data):
        # Extraemos los items del payload
        items_data = validated_data.pop('items')
        
        # 1. Obtenemos el usuario del contexto de la petición (request.user)
        # Esto soluciona el error IntegrityError: user_id NOT NULL
        user = self.context['request'].user
        
        # 2. Creamos la Orden asignándole el usuario
        order = Order.objects.create(user=user, **validated_data)

        # 3. Creamos los Items vinculados a la Orden
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order