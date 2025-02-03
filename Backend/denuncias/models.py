from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import User
from comunicaciones.models import Posteo, Evento
from django.utils.translation import gettext_lazy as _

class Denuncia(models.Model):
    TIPO_CHOICES = [
        ('spam', 'Spam'),
        ('inapropiado', 'Contenido Inapropiado'),
        ('ofensivo', 'Contenido Ofensivo'),
        ('acoso', 'Acoso'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('resuelta', 'Resuelta'),
        ('desestimada', 'Desestimada'),
    ]

    denunciante = models.ForeignKey(User,on_delete=models.CASCADE,related_name='denuncias_realizadas')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    usuario_denunciado = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='denuncias_recibidas')
    posteo_denunciado = models.ForeignKey(Posteo,null=True,blank=True,on_delete=models.CASCADE,related_name='denuncias')
    evento_denunciado = models.ForeignKey(Evento,null=True,blank=True,on_delete=models.CASCADE,related_name='denuncias')
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20,choices=ESTADO_CHOICES,default='pendiente')

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Denuncia'
        verbose_name_plural = 'Denuncias'

    def __str__(self):
        contenido = self.get_contenido_denunciado()
        return f"Denuncia {self.get_tipo_display()} - {contenido}"

    def get_contenido_denunciado(self):
        if self.usuario_denunciado:
            return f"Usuario: {self.usuario_denunciado}"
        elif self.posteo_denunciado:
            return f"Posteo: {self.posteo_denunciado}"
        elif self.evento_denunciado:
            return f"Evento: {self.evento_denunciado}"
        return None

    def clean(self):
        # Verificar que solo uno de los campos de contenido esté establecido
        contenidos = [
            self.usuario_denunciado,
            self.posteo_denunciado,
            self.evento_denunciado
        ]
        contenidos_establecidos = sum(1 for c in contenidos if c is not None)
        
        if contenidos_establecidos == 0:
            raise ValidationError(_('Debe especificar un contenido para denunciar.'))
        elif contenidos_establecidos > 1:
            raise ValidationError(_('Solo puede denunciar un contenido a la vez.'))

        # Verificar que el denunciante y el contenido denunciado pertenezcan al mismo edificio
        edificio_denunciante = self.denunciante.edificio
        edificio_denunciado = None

        if self.usuario_denunciado:
            edificio_denunciado = self.usuario_denunciado.edificio
        elif self.posteo_denunciado:
            edificio_denunciado = self.posteo_denunciado.usuario.edificio
        elif self.evento_denunciado:
            edificio_denunciado = self.evento_denunciado.usuario.edificio

        if edificio_denunciante != edificio_denunciado:
            raise ValidationError(_('Solo puedes denunciar contenido de tu mismo edificio.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


