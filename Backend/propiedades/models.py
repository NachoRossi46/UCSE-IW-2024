from django.db import models

class Edificio(models.Model):
    nombre = models.CharField(max_length=80)
    direccion = models.CharField(max_length=60)
    numero = models.IntegerField()
    ciudad = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.nombre} - {self.direccion} {self.numero}"
    

    




