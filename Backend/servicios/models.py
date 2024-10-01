from django.db import models
from propiedades.models import Edificio

class TipoServicio(models.Model):
    TIPO_CHOICE = [
        ('Plomeria', 'Plomeria'),
        ('Gasista', 'Gasista'),
        ('Electricista', 'Electricista'),
        ('Tecnico en Refrigeracion', 'Tecnico en Refrigeracion'),
        ('Cerrajero', 'Cerrajero'),
        ('Pintor', 'Pintor'),
    ]
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICE, unique=True)

    def __str__(self):
        return self.tipo

class Servicio(models.Model):
    tipo = models.ForeignKey(TipoServicio, on_delete=models.PROTECT)
    nombre_proveedor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    edificios = models.ManyToManyField(Edificio, related_name='servicios')

    def __str__(self):
        return f"{self.tipo} - {self.nombre_proveedor}"


