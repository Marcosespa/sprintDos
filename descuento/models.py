from django.db import models

class Descuento(models.Model):
    id_descuento = models.IntegerField(default=0)
    fecha_aplicacion = models.DateField(auto_now_add=True)
    valor_descuento = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Descuento {self.id_descuento} - Valor: {self.valor_descuento}"
