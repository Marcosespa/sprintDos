from django.db import models

# Create your models here.
class UsuarioPadreFamilia(models.Model):
    username = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    estudiante_relacionado = models.CharField(max_length=100)
    def __str__(self):
        return self.username