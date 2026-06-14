from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import action, display
from unfold.contrib.filters.admin import ChoicesDropdownFilter, DropdownFilter
from .models import Company
from unfold.contrib.filters.admin import ChoicesDropdownFilter, RangeDateTimeFilter


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    """
    Panel de administración premium para el modelo Company utilizando
    todas las capacidades extendidas y componentes visuales de Django Unfold.
    """

    # =================================================================
    # 1. CONFIGURACIÓN VISUAL DE LA TABLA PRINCIPAL (CHANGELIST)
    # =================================================================

    list_display = (
        'display_trade_name',
        'company_name',
        'rfc_company',
        'display_plan_saas',
        'display_subscription_status',
        'animal_limit',
        'created_at',
    )

    list_display_links = ('display_trade_name',)
    list_editable = ('animal_limit',)
    list_per_page = 20

    # =================================================================
    # 2. BUSCADORES Y FILTROS AVANZADOS
    # =================================================================

    search_fields = ('trade_name', 'company_name', 'rfc_company')

    list_filter = (
        ('plan_saaS', ChoicesDropdownFilter),
        ('subscription_status', ChoicesDropdownFilter),
        ('created_at', RangeDateTimeFilter),  # <-- Cambiado a RangeDateTimeFilter
    )

    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')

    # =================================================================
    # 3. DISEÑO DEL FORMULARIO DE EDICIÓN
    # =================================================================

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
            'fields': ('id', 'created_at', 'updated_at', 'deleted_at'),
        }),
    )

    # =================================================================
    # 4. ACCIONES MASIVAS PERSONALIZADAS
    # =================================================================

    actions = [
        'cambiar_plan_premium',
        'cambiar_plan_enterprise',
        'suspender_suscripcion',
        'activar_suscripcion',
    ]

    @action(description=_("Upgrade masivo: Cambiar plan a Premium"))
    def cambiar_plan_premium(self, request, queryset):
        queryset.update(plan_saaS='Premium')
        self.message_user(request, _("Los planes seleccionados han sido actualizados a Premium."))

    @action(description=_("Upgrade masivo: Cambiar plan a Enterprise"))
    def cambiar_plan_enterprise(self, request, queryset):
        queryset.update(plan_saaS='Enterprise')
        self.message_user(request, _("Los planes seleccionados han sido actualizados a Enterprise."))

    @action(description=_("🛑 Suspender suscripción por falta de pago"))
    def suspender_suscripcion(self, request, queryset):
        queryset.update(subscription_status='Suspendido')
        self.message_user(request, _("Las empresas seleccionadas han sido suspendidas correctamente."))

    @action(description=_("⚡ Reactivar suscripción de clientes"))
    def activar_suscripcion(self, request, queryset):
        queryset.update(subscription_status='Activo')
        self.message_user(request, _("Las suscripciones seleccionadas han sido reactivadas."))

    # =================================================================
    # 5. RENDERIZADORES COMPORTAMENTALES NATIVOS DE UNFOLD
    # =================================================================

    @display(description=_("Nombre Comercial"))
    def display_trade_name(self, obj):
        return obj.trade_name

    @display(description=_("Plan Contratado"), label=True)
    def display_plan_saas(self, obj):
        plan_styles = {
            'Básico': 'info',  # Azul claro
            'Premium': 'warning',  # Amarillo / Dorado
            'Enterprise': 'success'  # Verde esmeralda
        }
        return obj.plan_saaS, plan_styles.get(obj.plan_saaS, 'primary')

    @display(description=_("Estado Suscripción"), label=True)
    def display_subscription_status(self, obj):
        status_styles = {
            'Prueba': 'info',
            'Activo': 'success',
            'Suspendido': 'danger',  # Rojo
            'Cancelado': 'primary'  # Gris / Oscuro
        }
        return obj.get_subscription_status_display(), status_styles.get(obj.subscription_status, 'primary')
