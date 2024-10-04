from django.db import models

from descuento.models import Descuento
from recibo.models import Recibo
from usuarioPadreFamilia.models import UsuarioPadreFamilia

class Pago(models.Model):
    ESTADO_PAGO_CHOICES = [
        ('COMPLETADO', 'Completado'),
        ('PENDIENTE', 'Pendiente'),
        ('CANCELADO', 'Cancelado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    id_pago = models.AutoField(primary_key=True)
    fecha_pago = models.DateField()
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=15, choices=ESTADO_PAGO_CHOICES, default='PENDIENTE')
    tipo_pago = models.CharField(max_length=100)
    nombre_pago = models.CharField(max_length=100)
    usuario = models.ForeignKey(UsuarioPadreFamilia, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Pago {self.id_pago} - {self.nombre_pago}"