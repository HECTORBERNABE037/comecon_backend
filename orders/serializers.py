from rest_framework import serializers
from .models import Order, OrderItem, Cart
from catalog.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', 'product_details']
        extra_kwargs = {'product': {'write_only': True}}

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_moment', 'product_title', 'product_image']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_email', 'total', 'status', 'date', 'delivery_time', 'history_notes', 'items']