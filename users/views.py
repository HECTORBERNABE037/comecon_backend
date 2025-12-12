from rest_framework import viewsets, status, generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Card
from .serializers import UserSerializer, LoginSerializer, CardSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        
        # Devolvemos el token Y los datos del usuario (como espera tu App)
        user_data = UserSerializer(user).data
        return Response({'token': token.key, 'user': user_data})

class UserProfileView(generics.RetrieveUpdateAPIView):
    # Ver y editar perfil propio
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Validar límite de 3 tarjetas
        if Card.objects.filter(user=self.request.user).count() >= 3:
            raise serializers.ValidationError("Límite de 3 tarjetas alcanzado.")
        serializer.save(user=self.request.user)