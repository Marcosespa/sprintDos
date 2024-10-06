from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UsuarioPadreFamilia(models.Model):
    username = models.CharField(max_length=50, unique=True)
    contrasenia = models.CharField(max_length=128)  # Almacenar hashes de contraseña
    descripcion = models.CharField(max_length=255, default='Sin descripción')
    estudiante_relacionado = models.CharField(max_length=100, default='No reconocido')
    
    def set_password(self, raw_password):
        self.contrasenia = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.contrasenia)

    def __str__(self):
        return self.username
