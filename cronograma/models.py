from django.db import models

# Create your models here.
class Cronograma(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mes = models.CharField(max_length=50)

    def __str__(self):
        return self.mes