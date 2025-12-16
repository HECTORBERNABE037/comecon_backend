from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")
    password_2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if password and password_2:
            # 1. Validar que coincidan
            if password != password_2:
                self.add_error('password_2', "Las contraseñas no coinciden")
            
            # 2. Validar seguridad (longitud, números, etc.) usando las reglas de Django
            try:
                validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password', error)

        return cleaned_data

    def save(self, commit=True):
        # Guardado manual limpio
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    # Formulario para editar usuario (muestra la contraseña encriptada como read-only)
    password = ReadOnlyPasswordHashField(
        label="Contraseña",
        help_text="Las contraseñas se guardan encriptadas. Para cambiarla, usa el enlace de arriba."
    )

    class Meta:
        model = User
        fields = '__all__'