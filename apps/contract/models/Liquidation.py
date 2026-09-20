from django.db import models
from apps.core.models import BaseModel
from apps.contract.models.Contracts import Contract

class Liquidation(BaseModel):

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        PAID = 'Paid', 'Paid'
        CANCELED = 'Canceled', 'Canceled'

    class TypeSharecropper(models.TextChoices):
        LAND = 'Land', 'Land'
        LIVESTOCK = 'Livestock', 'Livestock'
        AGRICULTURE = 'Agriculture', 'Agriculture'

    type_sharecropper = models.CharField(max_length=50, choices=TypeSharecropper.choices)
    liquidation_date = models.DateField()
    status = models.CharField(max_length=50, choices=Status.choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_profit = models.DecimalField(max_digits=10, decimal_places=2)
    obligations = models.TextField(blank=True, null=True)
    penalties = models.TextField(blank=True, null=True)
    expenses_borne = models.CharField(max_length=50, choices=Contract.ExpensesBorne.choices)
    signature_sharecropper = models.CharField(max_length=255, blank=True, null=True)
    signature_owner = models.CharField(max_length=255, blank=True, null=True)

    sharecropper = models.ForeignKey(
        "partners.Sharecropper",
        on_delete=models.PROTECT,
        related_name="Liquidation_liquidations",
    )
    
    class Meta:
        db_table = '"liquidation"."liquidations"'
        verbose_name = 'Liquidation'
        verbose_name_plural = 'Liquidations'