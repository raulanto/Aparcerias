from django.utils.translation import gettext_lazy as _
from unfold.decorators import action

@action(description=_("Upgrade masivo: Cambiar plan a Premium"))
def cambiar_plan_premium(modeladmin, request, queryset):
    queryset.update(plan_saaS='Premium')
    modeladmin.message_user(request, _("Los planes actualizados a Premium."))

@action(description=_("Upgrade masivo: Cambiar plan a Enterprise"))
def cambiar_plan_enterprise(modeladmin, request, queryset):
    queryset.update(plan_saaS='Enterprise')
    modeladmin.message_user(request, _("Los planes actualizados a Enterprise."))

@action(description=_("🛑 Suspender suscripción por falta de pago"))
def suspender_suscripcion(modeladmin, request, queryset):
    queryset.update(subscription_status='Suspendido')
    modeladmin.message_user(request, _("Empresas suspendidas correctamente."))

@action(description=_("⚡ Reactivar suscripción de clientes"))
def activar_suscripcion(modeladmin, request, queryset):
    queryset.update(subscription_status='Activo')
    modeladmin.message_user(request, _("Suscripciones reactivadas."))