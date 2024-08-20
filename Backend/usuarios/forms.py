from django import forms
from .models import User, Rol

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'nombre', 'apellido', 'password', 'confirm_password', 'rol']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir el rol de Administrador
        self.fields['rol'].queryset = Rol.objects.exclude(rol='Administrador')

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return confirm_password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) 
        user.is_active = False
        if commit:
            user.save()
        return user
