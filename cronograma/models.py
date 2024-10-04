from django.db import models

# Create your models here.
class Cronograma(models.Model):
    id_cronograma = models.AutoField(primary_key=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.CharField(max_length=50)

    def __str__(self):
        return f"Cronograma {self.id_cronograma} - {self.mes}"