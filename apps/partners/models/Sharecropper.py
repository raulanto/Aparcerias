from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.companies.models import Company
from apps.core.models import BaseModel
from .SharecropperManager import SharecropperManager


class Sharecropper(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Modelo de identidad principal.
    Extiende Django Auth y hereda la auditoría y Soft Delete de BaseModel.
    """

    class TypeChoices(models.TextChoices):
        PROPIETARIO = 'Propietario', 'Propietario'
        PRODUCTOR_INDIVIDUAL = 'Productor Individual', 'Productor Individual'
        EJIDO = 'Ejido', 'Ejido / Núcleo Agrario'
        EMPRESA = 'Empresa', 'Empresa / Rancho S.A.'
        COMPRADOR = 'Comprador', 'Comprador Recurrente'

    class StatusChoices(models.TextChoices):
        PROSPECTO = 'Prospecto', 'Prospecto'
        ACTIVO = 'Activo', 'Activo'
        BLOQUEADO = 'Bloqueado', 'Bloqueado'
        INACTIVO = 'Inactivo', 'Inactivo'

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='sharecropper_set',  # Nombre inverso único
        related_query_name='sharecropper',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='sharecropper_permissions_set',  # Nombre inverso único
        related_query_name='sharecropper',
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.PROTECT,
        related_name='users',
        null=True,  # Permitimos null únicamente para Superusuarios Globales del SaaS
        blank=True,
        help_text="Tenant al que pertenece este usuario dentro del SaaS"
    )

    # Quitamos el unique=True de aquí para manejarlo en el Meta (Multi-tenant)
    email = models.EmailField(max_length=100, unique=True)
    legal_name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=TypeChoices.choices)

    # Quitamos el unique=True de aquí para manejarlo en el Meta (Multi-tenant)
    rfc = models.CharField(max_length=13, null=True, blank=True)
    curp = models.CharField(max_length=18, null=True, blank=True)
    domicile = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    bank_clabe = models.CharField(max_length=18, null=True, blank=True) # Corregido a clabe

    trust_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    state = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.PROSPECTO)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = SharecropperManager()
    all_objects = models.Manager()

    USERNAME_FIELD = 'email'
    # Corregido con los nombres exactos de los campos en inglés
    REQUIRED_FIELDS = ['legal_name', 'type']

    class Meta:
        db_table = '"partners"."sharecropper"'
        verbose_name = 'Aparcero'
        verbose_name_plural = 'Aparceros'
        # REGLAS DE ORO SAAS: El correo y el RFC son únicos POR EMPRESA, no globales.
        constraints = [
            models.UniqueConstraint(fields=['rfc', 'company'], name='unique_rfc_per_company')
        ]

    def __str__(self):
        return f"{self.legal_name} ({self.type})"