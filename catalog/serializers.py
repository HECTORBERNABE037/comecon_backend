from rest_framework import serializers
from .models import Product, Promotion

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'promotional_price', 'start_date', 'end_date', 'visible']

class ProductSerializer(serializers.ModelSerializer):
    # Campo calculado para ver si hay promo activa
    promotion = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # CORRECCIÓN AQUÍ: Cambiamos 'is_active' por 'visible'
        fields = ['id', 'title', 'description', 'price', 'image', 'category', 'promotion', 'visible']

    def get_promotion(self, obj):
        promo = Promotion.objects.filter(product=obj).first()
        if promo:
            return {
                'id': promo.id,
                'discount_price': promo.promotional_price, # Asegúrate que coincida con tu modelo
                'start_date': promo.start_date,
                'end_date': promo.end_date,
                'description': promo.description, # ✅ Ahora esto funcionará
                'visible': promo.visible
            }
        return None

    def get_active_price(self, obj):
        if hasattr(obj, 'promotion') and obj.promotion.visible:
            return obj.promotion.promotional_price
        return obj.price