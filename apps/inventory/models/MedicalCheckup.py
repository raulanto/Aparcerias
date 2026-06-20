from django.db import models
from apps.core.models import BaseModel

class MedicalCheckup(BaseModel):
    date = models.DateField()
    class Status(models.TextChoices):
        GOOD = 'Good', 'Good'
        AVERAGE = 'Average', 'Average'
        BAD = 'Bad', 'Bad'
    status = models.CharField(max_length=50, choices=Status.choices)
    treatment = models.TextField(blank=True, null=True)
    veterian_id = models.IntegerField() #Relacion
