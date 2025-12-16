from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from .models import Order, OrderItem, Cart
from .serializers import OrderSerializer, CartSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Si el producto ya está, sumamos cantidad en lugar de duplicar fila
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        
        cart_item, created = Cart.objects.get_or_create(
            user=self.request.user, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'administrador':
            return Order.objects.all().order_by('-date')
        return Order.objects.filter(user=user).order_by('-date')

class CheckoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic # Transacción Atómica: O todo se guarda, o nada
    def post(self, request):
        user = request.user
        payment_details = request.data.get('payment_details', 'Sin detalles')
        
        # 1. Obtener items del carrito
        cart_items = Cart.objects.filter(user=user).select_related('product', 'product__promotion')
        
        if not cart_items.exists():
            return Response({"error": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Calcular total 
        total = 0
        order_items_to_create = []
        
        for item in cart_items:
            # Precio: Promo si existe, sino Precio base
            if hasattr(item.product, 'promotion') and item.product.promotion.visible:
                price = item.product.promotion.promotional_price
            else:
                price = item.product.price
                
            total += price * item.quantity
            
            order_items_to_create.append(
                OrderItem(
                    order=None, 
                    product=item.product,
                    quantity=item.quantity,
                    price_at_moment=price
                )
            )

        # 3. Crear la Orden
        order = Order.objects.create(
            user=user,
            total=total,
            status='Pendiente',
            history_notes=payment_details,
            delivery_time="Calculando..."
        )

        # 4. Asignar items a la orden y guardar 
        for item in order_items_to_create:
            item.order = order
        
        OrderItem.objects.bulk_create(order_items_to_create)

        # 5. Vaciar Carrito
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)