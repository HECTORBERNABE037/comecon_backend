from rest_framework import serializers
from .models import Product, Promotion

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'promotional_price', 'start_date', 'end_date', 'visible']

class ProductSerializer(serializers.ModelSerializer):
    # Incluimos la promoción anidada 
    promotion = PromotionSerializer(read_only=True)
    
    # Campo calculado para saber el precio activo (Base vs Promo)
    active_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'subtitle', 'price', 'description', 
            'image', 'category', 'visible', 'promotion', 'active_price'
        ]

    def get_active_price(self, obj):
        if hasattr(obj, 'promotion') and obj.promotion.visible:
            return obj.promotion.promotional_price
        return obj.price