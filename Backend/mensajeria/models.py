from django.db import models
from usuarios.models import User

class Conversacion(models.Model):
    participantes = models.ManyToManyField(User, related_name='conversaciones')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ultima_actualizacion']

    def __str__(self):
        return f"Conversación {self.id} - {', '.join(user.email for user in self.participantes.all())}"

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha_envio']

    def __str__(self):
        return f"Mensaje de {self.remitente.email} - {self.fecha_envio}"


