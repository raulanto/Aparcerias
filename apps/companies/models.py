import uuid
from django.db import models
from apps.core.models import BaseModel


class Company(BaseModel):
    """
    Modelo Tenant principal para el esquema SaaS.
    Delimita de forma absoluta toda la información del sistema.
    """

    class PlanSaaS(models.TextChoices):
        BASICO = 'Básico', 'Básico'
        PREMIUM = 'Premium', 'Premium'
        ENTERPRISE = 'Enterprise', 'Enterprise'

    class SubscriptionStatus(models.TextChoices):
        PRUEBA = 'Prueba', 'Período de Prueba'
        ACTIVO = 'Activo', 'Suscripción Activa'
        SUSPENDIDO = 'Suspendido', 'Suspendido por Falta de Pago'
        CANCELADO = 'Cancelado', 'Suscripción Cancelada'

    trade_name = models.CharField(max_length=200, help_text="Nombre del Rancho o Empresa")
    company_name = models.CharField(max_length=200, null=True, blank=True, help_text="razon social de la empresa")
    rfc_company = models.CharField(max_length=13, unique=True, null=True, blank=True)
    plan_saaS = models.CharField(max_length=50, default='Básico', choices=PlanSaaS.choices)
    subscription_status = models.CharField(max_length=30, choices=SubscriptionStatus.choices,
                                           default=SubscriptionStatus.PRUEBA)
    animal_limit = models.IntegerField(default=100, help_text="Límite permitido por el plan")

    class Meta:
        db_table = '"companies"."company"'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return f"{self.trade_name}" (f"{self.get_subscription_status_display()}")
