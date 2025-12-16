from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    # Desactivamos username
    username = None 
    email = models.EmailField(unique=True)
    
    nickname = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[('administrador', 'Administrador'), ('cliente', 'Cliente')], default='cliente')
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    allow_notifications = models.BooleanField(default=True)
    allow_camera = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Sin username

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    last_four = models.CharField(max_length=4)
    holder_name = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=5)
    type = models.CharField(max_length=20)

    def __str__(self):
        return f"Tarjeta {self.type} - {self.last_four}"