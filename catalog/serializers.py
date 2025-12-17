from rest_framework import serializers
from .models import Product, Promotion

class PromotionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Promotion
        fields = ['id', 'product', 'promotional_price', 'start_date', 'end_date', 'description', 'visible']

class ProductSerializer(serializers.ModelSerializer):
    # Campo calculado para ver si hay promo activa
    promotion = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'image', 'category', 'promotion', 'visible']

    def get_promotion(self, obj):
        # TRAER LA PRIMERA, SIN IMPORTAR SI ES VISIBLE O NO
        promo = Promotion.objects.filter(product=obj).first()
        
        if promo:
            return {
                'id': promo.id,
                'discount_price': promo.promotional_price,
                'start_date': promo.start_date,
                'end_date': promo.end_date,
                'description': promo.description,
                'visible': promo.visible 
            }
        return None

    def get_active_price(self, obj):
        if hasattr(obj, 'promotion') and obj.promotion.visible:
            return obj.promotion.promotional_price
        return obj.price