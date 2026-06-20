from django.db import models
from apps.core.models import BaseModel

class Group(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    sharecropper_id = models.IntegerField() #Relacionar con Sharecropper
    