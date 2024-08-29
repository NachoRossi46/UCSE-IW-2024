from django.db import models
from usuarios.models import User

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


