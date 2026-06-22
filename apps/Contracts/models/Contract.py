from django.db import models
from apps.core.models import TenantModel


class Contract(TenantModel):
    """
    Representa el acuerdo principal de aparceria entre la empresa y un aparcero.
    """

    class StatusChoices(models.TextChoices):
        DRAFT = 'Borrador', 'Borrador'
        ACTIVE = 'Activo', 'Activo'
        FINISHED = 'Finalizado', 'Finalizado'
        CANCELLED = 'Cancelado', 'Cancelado'

    sharecropper = models.ForeignKey(
        'partners.Sharecropper',
        on_delete=models.PROTECT,
        related_name='contracts',
        help_text='Aparcero vinculado a este contrato'
    )
    start_date = models.DateField(help_text='Fecha de inicio del contrato')
    end_date = models.DateField(null=True, blank=True, help_text='Fecha de finalizacion del contrato')
    crop_or_activity = models.CharField(max_length=150, help_text='Cultivo o actividad principal del contrato')
    land_description = models.TextField(null=True, blank=True, help_text='Descripcion del terreno o unidad productiva')
    sharecropper_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    company_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=30,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = '"contracts"."contract"'
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return f"Contrato {self.sharecropper} - {self.status}"
