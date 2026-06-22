import uuid
from django.db import models
from django.utils import timezone

class ActiveManager(models.Manager):
    """Manager por defecto que filtra registros eliminados lógicamente."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class BaseModel(models.Model):
    """
    Modelo base abstracto con identificador UUID, timestamps
    y soporte nativo para borrado lógico (Soft Delete).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Managers
    objects = ActiveManager()         # Solo trae los activos por defecto
    all_objects = models.Manager()    # Acceso completo a la tabla

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, using=None, keep_parents=False):
        """Sobrescribe el borrado duro por un borrado lógico."""
        self.deleted_at = timezone.now()
        # update_fields optimiza la consulta SQL tocando solo la columna necesaria
        self.save(update_fields=['deleted_at'])

    def restore(self):
        """Restaura un registro borrado lógicamente."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])