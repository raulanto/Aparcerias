from django.db import models
from .BaseModel import BaseModel


class TenantModel(BaseModel):
    """
    Clase abstracta obligatoria para todos los modelos del sistema operativos.
    Garantiza que cada registro de ganado o finanzas esté etiquetado con su Tenant.
    """
    empresa = models.ForeignKey(
        'compañias.Empresa',
        on_delete=models.PROTECT,
        help_text="Empresa dueña de este registro de datos"
    )

    class Meta:
        abstract = True