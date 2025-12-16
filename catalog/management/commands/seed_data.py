import os
from django.core.management.base import BaseCommand
from django.core.files import File  # <--- Importante
from django.conf import settings
from users.models import User
from catalog.models import Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Carga datos iniciales con imágenes locales'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Iniciando sembrado con imágenes...")


        IMAGES_DIR = os.path.join(settings.BASE_DIR, 'semilla_img')


        if not User.objects.filter(email='admin1@comecon.com').exists():
            User.objects.create_superuser(
                email='admin1@comecon.com', password='password123',
                first_name='Samantha', last_name='Rios', role='administrador'
            )
            self.stdout.write("✅ Admin creado")

        if not User.objects.filter(email='cliente1@comecon.com').exists():
            User.objects.create_user(
                email='cliente1@comecon.com', password='password123',
                first_name='Juan', last_name='Pérez', role='cliente'
            )
            self.stdout.write("✅ Cliente creado")


        products_data = [
            {
                'title': 'Bowl con Frutas',
                'subtitle': 'Fresa, kiwi, avena',
                'price': 120.99,
                'description': 'Bowl fresco con frutas.',
                'image_filename': 'bowlFrutas.png', 
                'category': 'Desayunos'
            },
            {
                'title': 'Tostada',
                'subtitle': 'Aguacate',
                'price': 150.80,
                'description': 'Tostada integral con aguacate.',
                'image_filename': 'tostadaAguacate.png',
                'category': 'Comidas'
            },
            {
                'title': 'Panqueques',
                'subtitle': 'Avena y Frutas',
                'price': 115.99,
                'description': 'Torre de panqueques con miel.',
                'image_filename': 'Panques.png',
                'category': 'Desayunos'
            },
            {
                'title': 'Cafe Panda',
                'subtitle': 'Latte',
                'price': 110.00,
                'description': 'Café latte artesanal.',
                'image_filename': 'cafePanda.png',
                'category': 'Bebidas'
            }
        ]

        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                title=p_data['title'],
                defaults={
                    'subtitle': p_data['subtitle'],
                    'price': Decimal(str(p_data['price'])),
                    'description': p_data['description'],
                    'category': p_data['category'],
                    'visible': True
                }
            )

            if created or not product.image:
                image_path = os.path.join(IMAGES_DIR, p_data['image_filename'])
                
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        product.image.save(p_data['image_filename'], File(f), save=True)
                        self.stdout.write(f"   📸 Imagen cargada para: {product.title}")
                else:
                    self.stdout.write(f"   ⚠️ No se encontró la imagen: {image_path}")
            
            if created:
                self.stdout.write(f"✅ Producto creado: {product.title}")
            else:
                self.stdout.write(f"ℹ️ Producto actualizado: {product.title}")

        self.stdout.write(self.style.SUCCESS('✨ Sembrado completo.'))