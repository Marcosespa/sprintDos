from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioPadreFamiliaManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario debe ser obligatorio')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class UsuarioPadreFamilia(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    contrasenia = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, default='Sin descripción')
    estudiante_relacionado = models.CharField(max_length=100, default='No reconocido')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioPadreFamiliaManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.username
