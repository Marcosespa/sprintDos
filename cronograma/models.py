# models.py
from django.db import models
from descuento.models import Descuento
from recibo.models import Recibo
from usuarioPadreFamilia.models import UsuarioPadreFamilia

class Cronograma(models.Model):
    mes = models.CharField(max_length=20)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado_pago = models.CharField(max_length=20, default='PENDIENTE')
    usuario_padre = models.ForeignKey(UsuarioPadreFamilia, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.mes} - {self.estado_pago}"

class Pago(models.Model):
    fecha_pago = models.DateField()
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado_pago = models.CharField(
        max_length=20,
        choices=[
            ('COMPLETADO', 'Completado'),
            ('PENDIENTE', 'Pendiente'),
            ('CANCELADO', 'Cancelado'),
            ('RECHAZADO', 'Rechazado')
        ],
        default='PENDIENTE'
    )
    tipo_pago = models.CharField(max_length=100, default="")
    nombre_pago = models.CharField(max_length=100, default="Pago genérico")
    
    descuentos = models.ManyToManyField(Descuento, related_name='pagos_cronograma_app') 
    recibo = models.OneToOneField(Recibo, null=True, blank=True, on_delete=models.CASCADE, related_name='pago_cronograma_app') 
    cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE, null=True, blank=True, related_name='pagos_asociados')
    usuario_padre = models.ForeignKey(UsuarioPadreFamilia, on_delete=models.CASCADE, null=True, blank=True, related_name='pagos_asociados')

    def __str__(self):
        return f"Pago de {self.nombre_pago} - {self.valor_pago}"
