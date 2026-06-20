from django.db import models
from apps.core.models import BaseModel

class Weighing(BaseModel):
    date = models.DateField()
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    daily_earnings = models.DecimalField(max_digits=10, decimal_places=2)