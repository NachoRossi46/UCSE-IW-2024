from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from propiedades.models import Edificio
from django.utils import timezone
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Completar el campo email. '))
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser debe tener is_superuser=True.'))


        admin_rol, _ = Rol.objects.get_or_create(rol='Administrador')
        extra_fields['rol'] = admin_rol
        
        return self.create_user(email, nombre, apellido, password, **extra_fields)


class Rol(models.Model):
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Colaborador', 'Colaborador'),
        ('Inquilino', 'Inquilino'),
        ('Duenio', 'Duenio'),
    ]
    
    rol = models.CharField(max_length=30, choices=ROL_CHOICES, unique=True)

    def __str__(self):
        return self.rol

class User(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=False, null=False)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios')
    edificio = models.ForeignKey(Edificio, on_delete=models.SET_NULL, null=True, related_name='usuarios')
    piso = models.IntegerField(null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.is_superuser and self.rol.rol != 'Administrador':
            admin_rol, _ = Rol.objects.get_or_create(rol='Administrador')
            self.rol = admin_rol
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # El token expira después de 1 hora
        return not self.is_used and (timezone.now() - self.created_at).seconds < 3600
