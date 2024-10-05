from django.db import models

# Create your models here.
class Recibo(models.Model):
    ESTADO_RECIBO_CHOICES = [
        ('VENCIDO', 'Vencido'),
        ('POR PAGAR', 'Por pagar'),
        ('PAGADO', 'Pagado'),
    ]

    id_recibo = models.IntegerField(default=0)

    fecha_emision = models.DateField()
    codigo_barras = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=10, choices=ESTADO_RECIBO_CHOICES, default='POR PAGAR')
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()

    def __str__(self):
        return f"Recibo {self.id_recibo} - {self.estado}"