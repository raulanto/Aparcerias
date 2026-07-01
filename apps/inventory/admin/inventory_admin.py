from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import ChoicesDropdownFilter

from apps.core.admin import BaseSaaSAdmin
from ..models import Animal, Group, MedicalCheckup, Weighing


@admin.register(Group)
class GroupAdmin(BaseSaaSAdmin):
    list_display = ('name', 'sharecropper', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name', 'description', 'sharecropper__legal_name', 'sharecropper__email')
    list_filter = ('sharecropper', 'created_at')
    autocomplete_fields = ('sharecropper',)

    fieldsets = (
        (_('Informacion del lote'), {
            'classes': ('tab',),
            'fields': ('name', 'description', 'sharecropper'),
        }),
        (_('Auditoria del sistema'), {
            'classes': ('collapse',),
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at'),
        }),
    )


@admin.register(Animal)
class AnimalAdmin(BaseSaaSAdmin):
    readonly_fields = BaseSaaSAdmin.readonly_fields + ('ingression_date',)

    list_display = (
        'id', 'specie', 'breed', 'sex', 'group',
        'birth_date', 'ingression_date', 'current_price',
    )
    list_display_links = ('id',)
    search_fields = ('id', 'description', 'notes', 'group__name')
    list_filter = (
        ('specie', ChoicesDropdownFilter),
        ('breed', ChoicesDropdownFilter),
        ('sex', ChoicesDropdownFilter),
        'group',
        'ingression_date',
    )
    autocomplete_fields = ('group',)

    fieldsets = (
        (_('Identificacion biologica'), {
            'classes': ('tab',),
            'fields': ('specie', 'breed', 'sex', 'birth_date', 'description'),
        }),
        (_('Operacion'), {
            'classes': ('tab',),
            'fields': ('group', 'ingression_date', 'buy_price', 'current_price', 'notes'),
        }),
        (_('Auditoria del sistema'), {
            'classes': ('collapse',),
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at'),
        }),
    )


@admin.register(Weighing)
class WeighingAdmin(BaseSaaSAdmin):
    list_display = ('animal', 'date', 'weight_kg', 'daily_earnings', 'created_at')
    list_display_links = ('animal', 'date')
    search_fields = ('animal__id', 'animal__group__name')
    list_filter = ('date', 'animal__group')
    autocomplete_fields = ('animal',)

    fieldsets = (
        (_('Pesaje'), {
            'classes': ('tab',),
            'fields': ('animal', 'date', 'weight_kg', 'daily_earnings'),
        }),
        (_('Auditoria del sistema'), {
            'classes': ('collapse',),
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at'),
        }),
    )


@admin.register(MedicalCheckup)
class MedicalCheckupAdmin(BaseSaaSAdmin):
    list_display = ('animal', 'date', 'status', 'veterinarian_id', 'created_at')
    list_display_links = ('animal', 'date')
    search_fields = ('animal__id', 'animal__group__name', 'treatment')
    list_filter = (('status', ChoicesDropdownFilter), 'date', 'animal__group')
    autocomplete_fields = ('animal',)

    fieldsets = (
        (_('Revision sanitaria'), {
            'classes': ('tab',),
            'fields': ('animal', 'date', 'status', 'treatment', 'veterinarian_id'),
        }),
        (_('Auditoria del sistema'), {
            'classes': ('collapse',),
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at'),
        }),
    )
