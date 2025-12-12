from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Card

class CustomUserAdmin(UserAdmin):
    # Conectamos los formularios
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    # Configuraciones para usar Email en lugar de Username
    username = None
    ordering = ('email',)
    list_display = ('email', 'first_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name')

    # 1. PANTALLA DE CREACIÓN (Add User)
    # Aquí es donde DEBEN estar password y password_2 para que se vean
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'first_name', 
                'last_name', 
                'role', 
                'password',    # <--- IMPORTANTE: Debe estar aquí
                'password_2'   # <--- IMPORTANTE: Debe estar aquí
            ),
        }),
    )

    # 2. PANTALLA DE EDICIÓN (Change User)
    # Aquí definimos cómo se ve un usuario ya creado
    fieldsets = (
        ('Información de Cuenta', {'fields': ('email', 'password')}),
        ('Datos Personales', {'fields': ('first_name', 'last_name', 'nickname', 'phone', 'gender', 'image')}),
        ('Dirección', {'fields': ('country', 'address')}),
        ('Permisos', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Configuración', {'fields': ('allow_notifications', 'allow_camera')}),
    )

admin.site.register(User, CustomUserAdmin)

# Registro simple para Tarjetas
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('type', 'last_four', 'user', 'expiry_date')