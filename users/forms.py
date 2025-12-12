from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    # Declaramos los campos de contraseña explícitamente
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")
    password_2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar contraseña")

    class Meta:
        model = User
        # CORRECCIÓN: Solo incluimos campos REALES de la base de datos aquí.
        # Quitamos password y password_2 de esta lista (ya están declarados arriba).
        fields = ('email', 'first_name', 'last_name', 'role')

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password_2")
        if p1 and p2 and p1 != p2:
            self.add_error('password_2', "Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        # Guardamos el usuario sin commit primero
        user = super(UserCreationForm, self).save(commit=False)
        # Asignamos la contraseña encriptada
        user.set_password(self.cleaned_data["password"])
        # Asignamos otros campos si es necesario
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'