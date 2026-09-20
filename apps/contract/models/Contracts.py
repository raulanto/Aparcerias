from django.db import models
from apps.core.models import BaseModel

class Contract(BaseModel):

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ACTIVE = 'Active', 'Active'
        FINISHED = 'Finished', 'Finished'
        CANCELED = 'Canceled', 'Canceled'

    class TypeSharecropper(models.TextChoices):
        LAND = 'Land', 'Land'
        LIVESTOCK = 'Livestock', 'Livestock'
        AGRICULTURE = 'Agriculture', 'Agriculture'

    class ExpensesBorne(models.TextChoices):
        SHARECROPPER = 'Sharecropper', 'Sharecropper'
        OWNER = 'Owner', 'Owner'
        BOTH = 'Both', 'Both'

    type_sharecropper = models.CharField(max_length=50, choices=TypeSharecropper.choices)
    start_date = models.DateField()
    finish_date = models.DateField()
    status = models.CharField(max_length=50, choices=Status.choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_profit = models.DecimalField(max_digits=10, decimal_places=2)
    obligations = models.TextField(blank=True, null=True)
    penalties = models.TextField(blank=True, null=True)
    expenses_borne = models.CharField(max_length=50, choices=ExpensesBorne.choices)
    signature_sharecropper = models.CharField(max_length=255, blank=True, null=True)
    signature_owner = models.CharField(max_length=255, blank=True, null=True)



    sharecropper = models.ForeignKey(
        "partners.Sharecropper",
        on_delete=models.PROTECT,
        related_name="Contract_contracts",
    )
    class Meta:
        db_table = '"contract"."contracts"'
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'