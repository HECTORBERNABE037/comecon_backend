from django.contrib import admin
from .models import Order, OrderItem, Cart

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product'] 
    extra = 0 # No mostrar filas vacías extra

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'date', 'delivery_time')
    list_filter = ('status', 'date')
    search_fields = ('user__email', 'id')
    readonly_fields = ('date',)
    inlines = [OrderItemInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__email', 'product__title')