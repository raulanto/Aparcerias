from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import ChoicesDropdownFilter, RangeDateTimeFilter

# Importamos nuestras abstracciones
from apps.core.admin import BaseSaaSAdmin
from ..models import Company
from .mixins import CompanyDisplayMixin
from .actions import cambiar_plan_premium,cambiar_plan_enterprise,activar_suscripcion,suspender_suscripcion


@admin.register(Company)
class CompanyAdmin(BaseSaaSAdmin, CompanyDisplayMixin):
    """
    Panel de configuración. Exclusivamente para enrutamiento (Wiring).
    """

    list_display = (
        'display_trade_name', 'company_name', 'rfc_company',
        'display_plan_saas', 'display_subscription_status',
        'animal_limit', 'created_at',
    )
    list_display_links = ('display_trade_name',)
    list_editable = ('animal_limit',)

    search_fields = ('trade_name', 'company_name', 'rfc_company')
    list_filter = (
        ('plan_saaS', ChoicesDropdownFilter),
        ('subscription_status', ChoicesDropdownFilter),
        ('created_at', RangeDateTimeFilter),
    )

    fieldsets = (
        (_('Identidad Corporativa'), {
            'classes': ('tab',),
            'fields': ('trade_name', 'company_name', 'rfc_company'),
        }),
        (_('Configuración SaaS & Suscripción'), {
            'classes': ('tab',),
            'fields': ('plan_saaS', 'subscription_status', 'animal_limit'),
        }),
        (_('Auditoría del Sistema'), {
            'classes': ('collapse',),
            # Los campos reales ya vienen heredados de BaseSaaSAdmin
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at'),
        }),
    )

    # Inyectamos los Casos de Uso (Actions)
    actions = [
        cambiar_plan_premium,
        cambiar_plan_enterprise,
        suspender_suscripcion,
        activar_suscripcion,
    ]