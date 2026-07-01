from django.db import models
from apps.core.models import BaseModel

class Animal(BaseModel):

    class  Species(models.TextChoices):
        BOVINO = 'Bovino', 'Bovino'
        OVINO = 'Ovino', 'Ovino'
        CAPRINO = 'Caprino', 'Caprino'
        EQUINO = 'Equino', 'Equino'
        PORCINO = 'Porcino', 'Porcino'

    class Breeds (models.TextChoices):
        ANGUS = 'Angus', 'Angus'
        HEREFORD = 'Hereford', 'Hereford'
        HOLSTEIN = 'Holstein', 'Holstein'
        SANTA_GERTRUDIS = 'Santa Gertrudis', 'Santa Gertrudis'
        CHAROLAIS = 'Charolais', 'Charolais',
        SIMMENTAL = 'Simmental', 'Simmental',
        LIMOUSIN = 'Limousin', 'Limousin',

    class Sexs(models.TextChoices):
        MACHO = 'Macho', 'Macho'
        HEMBRA = 'Hembra', 'Hembra'

    class Porpuse(models.TextChoices):
        CRIA = 'Cría', 'Cría'
        ENGORDE = 'Engorde', 'Engorde'
        LECHE = 'Leche', 'Leche'
        DOBLE_PROPOSITO = 'Doble Propósito', 'Doble Propósito'
        REPRODUCTOR = 'Reproductor', 'Reproductor'

    specie = models.CharField(max_length=50, choices=Species.choices)
    breed = models.CharField(max_length=50, choices=Breeds.choices)
    sex = models.CharField(max_length=50, choices=Sexs.choices)
    birth_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    #contract:  relacion con tabla de Contratos "Contracts"
    ingression_date = models.DateField(auto_now_add=True)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    #picture: Identificacion visual(URL)
    notes = models.TextField(blank=True, null=True)

    # Esto debe ser una tabla intermedia
    group = models.ForeignKey( 
        "inventory.Group",
        on_delete=models.PROTECT,
        related_name="animals",
    )
    class Meta: # type: ignore
        db_table = '"inventory"."animal"'
        verbose_name = 'Animal'
        verbose_name_plural = 'Animales'
    
