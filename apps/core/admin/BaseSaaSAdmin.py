from unfold.admin import ModelAdmin

class BaseSaaSAdmin(ModelAdmin):
    """
    Clase base para todos los modelos del SaaS.
    Estandariza la paginación y protege la auditoría.
    """
    list_per_page = 20
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')