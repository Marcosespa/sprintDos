from django.db import models

# Create your models here.
class Descuento(models.Model):
    fecha_aplicacion = models.DateField()
    valor_descuento = models.FloatField()

    def __str__(self):
        return self.fecha_aplicacion