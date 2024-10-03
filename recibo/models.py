from django.db import models

# Create your models here.
class Recibo(models.Model):
    fecha_emision = models.DateField()
    codigo_barras = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    saldo_pendiente = models.FloatField()
    descripcion = models.CharField(max_length=100)


    def __str__(self):
        return self.fecha_emision