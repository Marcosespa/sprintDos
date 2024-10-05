from django.db import models

from cronograma.models import Cronograma

# Create your models here.
class UsuarioPadreFamilia(models.Model):
    username = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, default='Sin descripción')
    estudiante_relacionado = models.CharField(max_length=100)
    def __str__(self):
        return self.username
        return self.username