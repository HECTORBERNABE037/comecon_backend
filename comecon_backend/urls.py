from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Importamos las vistas que creamos en los pasos anteriores
from users.views import RegisterView, LoginView, UserProfileView, CardViewSet, CheckEmailView, ResetPasswordView
from catalog.views import ProductViewSet, PromotionViewSet
from orders.views import CartViewSet, OrderViewSet, CheckoutView


# 1. Configuración del Router
# El router crea automáticamente las URLs para los ViewSets 
router = DefaultRouter()

# Users App
router.register(r'cards', CardViewSet, basename='cards') # /api/cards/
router.register(r'orders', OrderViewSet, basename='orders') # /api/orders/
router.register(r'products', ProductViewSet, basename='products') # /api/products/

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

    #Auth
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    
    #recuperacion de contraseña
    path('api/check-email/', CheckEmailView.as_view(), name='check_email'),
    path('api/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    
    #perfil y pagos
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/checkout/', CheckoutView.as_view(), name='checkout'),

    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)