from django.db import models
from django.conf import settings
from catalog.models import Product # Importamos el modelo de Producto

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendiente')
    date = models.DateField(auto_now_add=True) # Se guarda la fecha automáticamente al crear
    delivery_time = models.CharField(max_length=100, blank=True, null=True)
    history_notes = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # Si se borra el producto, no se borra el historial de ventas
    quantity = models.PositiveIntegerField(default=1)
    price_at_moment = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Guardamos el precio al momento de la compra 
    price_at_moment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # Evita que el mismo usuario tenga 2 filas para el mismo producto (debe sumar cantidad, no crear nueva fila)
        unique_together = ('user', 'product')

    def __str__(self):
        return f"Carrito: {self.user.email} - {self.product.title} ({self.quantity})"