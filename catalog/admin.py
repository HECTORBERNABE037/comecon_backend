from django.contrib import admin
from .models import Product, Promotion

class PromotionInline(admin.StackedInline):
    model = Promotion
    can_delete = False
    verbose_name_plural = 'Promoción Activa'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'visible', 'has_promo')
    list_filter = ('category', 'visible')
    search_fields = ('title', 'description')
    
    # Permite editar la promoción directamente desde la pantalla del producto
    inlines = [PromotionInline]

    def has_promo(self, obj):
        return hasattr(obj, 'promotion') and obj.promotion.visible
    has_promo.boolean = True
    has_promo.short_description = 'En Oferta'

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('product', 'promotional_price', 'visible', 'start_date', 'end_date')