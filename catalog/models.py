from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    # Imagen del producto (se guardará en 'media/products/')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    category = models.CharField(max_length=100, blank=True, null=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Promotion(models.Model):
    # Relación 1 a 1: Un producto puede tener solo una promoción activa a la vez 
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='promotion')
    promotional_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    visible = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    #image = models.ImageField(upload_to='promos/', blank=True, null=True)

    def __str__(self):
        return f"Promo: {self.product.title} a ${self.promotional_price}"