from django.db import models
from apps.core.models import BaseModel

class Group(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    
    sharecropper = models.ForeignKey(
        "partners.Sharecropper",
        on_delete=models.PROTECT,
        related_name="inventory_groups",
    )

    class Meta: # type: ignore
        db_table = '"inventory"."group"'
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
    