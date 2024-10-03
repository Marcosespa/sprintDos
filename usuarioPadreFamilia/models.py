from django.db import models

# Create your models here.
class UsuarioPadreFamilia(models.Model):
    user_name = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    estudiante_relacionado = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name