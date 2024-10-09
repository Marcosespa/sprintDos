from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.models import BaseUserManager

class UsuarioPadreFamiliaManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class UsuarioPadreFamilia(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Agregar related_name para evitar el conflicto con auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='usuarioPadreFamilia_set',  # Cambiar related_name
        blank=True,
        help_text='Los grupos a los que pertenece el usuario.',
        verbose_name='grupos'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarioPadreFamilia_permissions',  # Cambiar related_name
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos de usuario'
    )

    objects = UsuarioPadreFamiliaManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email
