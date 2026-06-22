from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

class CompanyDisplayMixin:
    """Capa de presentación (View Logic) para la empresa."""

    @display(description=_("Nombre Comercial"))
    def display_trade_name(self, obj):
        return obj.trade_name

    @display(description=_("Plan Contratado"), label=True)
    def display_plan_saas(self, obj):
        plan_styles = {
            'Básico': 'info',
            'Premium': 'warning',
            'Enterprise': 'success'
        }
        return obj.plan_saaS, plan_styles.get(obj.plan_saaS, 'primary')

    @display(description=_("Estado Suscripción"), label=True)
    def display_subscription_status(self, obj):
        status_styles = {
            'Prueba': 'info',
            'Activo': 'success',
            'Suspendido': 'danger',
            'Cancelado': 'primary'
        }
        return obj.get_subscription_status_display(), status_styles.get(obj.subscription_status, 'primary')