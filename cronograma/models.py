from django.db import models

# Create your models here.
class Cronograma(models.Model):
    mes = models.CharField(max_length=50)

    def __str__(self):
        return self.mes