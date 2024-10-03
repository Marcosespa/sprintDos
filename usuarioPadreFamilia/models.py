from django.db import models

from cronograma.models import Cronograma

# Create your models here.
class UsuarioPadreFamilia(models.Model):
    username = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=50)
    cronogramas = models.ManyToManyField(Cronograma)

    def __str__(self):
        return self.username