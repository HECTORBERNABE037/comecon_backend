from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Product, Promotion
from .serializers import ProductSerializer, PromotionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    
    # Cualquiera puede ver, solo Admin puede editar
    permission_classes = [IsAuthenticatedOrReadOnly] 

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAdminUser] # Solo admin gestiona promos