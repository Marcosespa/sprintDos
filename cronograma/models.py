# models.py
from django.db import models
from descuento.models import Descuento
from recibo.models import Recibo
from usuarioPadreFamilia.models import UsuarioPadreFamilia
from decimal import Decimal

class ConceptoPago(models.Model):
    TIPO_CHOICES = [
        ('MATRICULA', 'Matrícula'),
        ('MENSUALIDAD', 'Mensualidad'),
        ('MATERIALES', 'Materiales'),
        ('OTROS', 'Otros')
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    mes_aplicable = models.CharField(max_length=20)  # Mes al que aplica el concepto
    año_escolar = models.IntegerField()
    descripcion = models.TextField(blank=True)
    fecha_vencimiento = models.DateField()
    creado_por = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ['tipo', 'mes_aplicable', 'año_escolar']

class Cronograma(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Pago Parcial'),
        ('COMPLETADO', 'Completado'),
        ('VENCIDO', 'Vencido')
    ]
    
    año_escolar = models.IntegerField()
    mes = models.CharField(max_length=20)
    usuario_padre = models.ForeignKey('usuarioPadreFamilia.UsuarioPadreFamilia', on_delete=models.CASCADE)
    conceptos = models.ManyToManyField(ConceptoPago, through='CronogramaConcepto')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    
    @property
    def valor_total(self):
        return sum(concepto.valor for concepto in self.conceptos.all())
        
    @property
    def saldo_pendiente(self):
        pagos = self.pagos.filter(estado_pago='PAGADO')
        total_pagado = sum(pago.valor_pago for pago in pagos)
        return self.valor_total - total_pagado

class CronogramaConcepto(models.Model):
    cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE)
    concepto = models.ForeignKey(ConceptoPago, on_delete=models.CASCADE)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2)

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
