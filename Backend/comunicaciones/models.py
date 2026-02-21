from django.db import models
from usuarios.models import User
from django.core.exceptions import ValidationError

class TipoPosteo(models.Model):
    TIPO_CHOICES = [
        ('Reclamo', 'Reclamo'),
        ('Consulta', 'Consulta'),
        ('Aviso', 'Aviso'),
    ]

    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, unique=True)

    def __str__(self):
        return self.tipo


class Posteo(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='posteos')
    tipo_posteo = models.ForeignKey(TipoPosteo ,on_delete=models.PROTECT, related_name='posteos')
    imagen = models.ImageField(upload_to='posteos/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Respuesta(models.Model):
    posteo = models.ForeignKey(Posteo, on_delete=models.CASCADE, related_name='respuestas')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respuesta de {self.usuario} a {self.posteo}"


class TipoEvento(models.Model):
    TIPO_CHOICES = [
        ('Mantenimiento', 'Mantenimiento'),
        ('Limpieza', 'Limpieza'),
        ('Reformas', 'Reformas'),
        ('Reunion de Consorcio', 'Reunion de Consorcio'),
    ]
    
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, unique=True)
    
    def __str__(self):
        return self.tipo

class Evento(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos')
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.PROTECT, related_name='eventos')

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError(('La fecha y hora de fin debe ser igual o posterior a la fecha y hora de inicio.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

