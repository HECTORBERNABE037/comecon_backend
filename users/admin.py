from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Card

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    # Configuración de lista
    ordering = ('email',)
    list_display = ('email', 'first_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name')
    
    username = None

    # 1. PANTALLA DE CREACIÓN (Agregar Usuario)
    # Ahora que 'password' y 'password_2' están en forms.py, esto funcionará
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password', 'password_2'),
        }),
    )

    # 2. PANTALLA DE EDICIÓN
    fieldsets = (
        ('Credenciales', {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'nickname', 'phone', 'gender', 'image')}),
        ('Ubicación', {'fields': ('country', 'address')}),
        ('Permisos', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Configuración App', {'fields': ('allow_notifications', 'allow_camera')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('type', 'last_four', 'user', 'expiry_date')
    search_fields = ('user__email', 'last_four')