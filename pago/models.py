from django.db import models
from cronograma.models import Cronograma
from descuento.models import Descuento
from recibo.models import Recibo
from usuarioPadreFamilia.models import UsuarioPadreFamilia

class Pago(models.Model):
    fecha_pago = models.DateField()
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado_pago = models.CharField(max_length=20, default='PENDIENTE')

    tipo_pago = models.CharField(max_length=100, default='Pendiente')
    nombre_pago = models.CharField(max_length=100, default='Pago genérico')
    descuentos = models.ManyToManyField(Descuento, related_name='pagos_cronograma')
    recibo = models.OneToOneField(
        Recibo,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='pago_pago'
    )
    cronograma = models.ForeignKey(
        Cronograma,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pagos_asociados_pago'
    )
    usuario_padre = models.ForeignKey(
        UsuarioPadreFamilia,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pagos_asociados_pago'
    )

    def __str__(self):
        return f"Pago de {self.nombre_pago} - {self.valor_pago}"
