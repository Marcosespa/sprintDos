from django.db import models

from descuento.models import Descuento
from recibo.models import Recibo

class Pago(models.Model):
    fecha_pago = models.DateField()
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=100)
    descuentos = models.ManyToManyField(Descuento)
    recibo= models.OneToOneField(Recibo,null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha_pago

# Create your models here.
