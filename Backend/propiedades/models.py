from django.db import models
from usuarios.models import User
from django.core.exceptions import ValidationError

class Edificio(models.Model):
    nombre = models.CharField(max_length=100)
    # idCiudad = models.IntegerField()
    direccion = models.CharField(max_length=60)
    numero = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} - {self.direccion} {self.numero}"
    
class Departamento(models.Model):
    idDuenio = models.ForeignKey(User, related_name='departamentos_duenio', on_delete=models.SET_NULL, null=True, blank=True)
    idOcupante = models.ForeignKey(User, related_name='departamentos_ocupante', on_delete=models.SET_NULL, null=True, blank=True)
    piso = models.IntegerField()
    numero = models.CharField(max_length=10)
    idEdificio = models.ForeignKey(Edificio, related_name='departamentos', on_delete=models.CASCADE)
    ocupaDepto = models.BooleanField()

    def __str__(self):
        return f'Departamento {self.numero} - Piso {self.piso} en Edificio {self.idEdificio.nombre}'
    
    def clean(self):
        self.numero = self.numero.upper()

        super().clean()

        if self.idOcupante and not self.idDuenio:
            raise ValidationError("No se puede asignar un ocupante sin un dueño.")

        if self.idOcupante and self.ocupaDepto is not True:
            raise ValidationError("El campo 'ocupaDepto' debe estar en True cuando hay un ocupante asignado.")
        
        if Departamento.objects.filter(idEdificio=self.idEdificio, numero=self.numero).exclude(id=self.id).exists():
            raise ValidationError(f"Ya existe un departamento con el número {self.numero} en el edificio {self.idEdificio.nombre}.")




