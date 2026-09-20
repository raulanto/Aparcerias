from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from ..models import Sharecropper

# Opcional: Si quieres mantener los Grupos nativos de Django con el estilo de Unfold
admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    pass


@admin.register(Sharecropper)
class SharecropperAdmin(ModelAdmin):
    """
    Configuración del panel de Unfold para el modelo de usuario personalizado.
    """
    # 1. Campos a mostrar en la tabla principal
    list_display = ('email', 'legal_name', 'type', 'company', 'state', 'is_staff')

    # 2. Buscador y Filtros laterales
    search_fields = ('email', 'legal_name', 'rfc')
    list_filter = ('type', 'state', 'company', 'is_staff', 'is_superuser')

    # 3. Ordenamiento por defecto
    ordering = ('email',)

    # 4. Vista de Edición (Cuando abres un usuario ya creado)
    fieldsets = (
        ('Autenticación', {
            'fields': ('email', 'password')
        }),
        ('Información Comercial / Legal', {
            'fields': ('legal_name', 'type', 'company')
        }),
        ('Datos Fiscales y Contacto', {
            'fields': ('rfc', 'curp', 'domicile', 'phone', 'bank_clabe')
        }),
        ('Estado Operativo', {
            'fields': ('state', 'trust_rating')
        }),
        ('Permisos de Sistema', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)  # Unfold colapsará esta sección por defecto
        }),
    )

    # 5. Vista de Creación (Cuando le das al botón "Añadir Sharecropper")
    add_fieldsets = (
        ('Crear nuevo usuario', {
            'classes': ('wide',),
            'fields': ('email', 'legal_name', 'type', 'company', 'password'),
        }),
    )

    # 6. Para que los selectores múltiples de permisos se vean bien en Unfold
    filter_horizontal = ('groups', 'user_permissions')

    # Para encriptar la contraseña si se guarda desde el admin
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un usuario nuevo
            obj.set_password(obj.password)
        elif form.initial.get('password') != obj.password:  # Si cambiaron la contraseña
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)