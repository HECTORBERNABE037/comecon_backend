from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Importamos las vistas que creamos en los pasos anteriores
from users.views import RegisterView, LoginView, UserProfileView, CardViewSet
from catalog.views import ProductViewSet, PromotionViewSet
from orders.views import CartViewSet, OrderViewSet, CheckoutView

# 1. Configuración del Router
# El router crea automáticamente las URLs para los ViewSets (CRUDs completos)
router = DefaultRouter()

# Users App
router.register(r'cards', CardViewSet, basename='card') # /api/cards/

# Catalog App
router.register(r'products', ProductViewSet)            # /api/products/
router.register(r'promotions', PromotionViewSet)        # /api/promotions/

# Orders App
router.register(r'cart', CartViewSet, basename='cart')  # /api/cart/
router.register(r'orders', OrderViewSet, basename='order') # /api/orders/

# 2. Definición de URLs
urlpatterns = [
    # Panel de Administración de Django
    path('admin/', admin.site.urls),

    # --- Endpoints Personalizados (APIViews / Generics) ---
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/checkout/', CheckoutView.as_view(), name='checkout'),

    # --- Endpoints del Router (Incluye todas las rutas registradas arriba) ---
    path('api/', include(router.urls)),
]

# 3. Configuración para servir imágenes en modo desarrollo (Local)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)