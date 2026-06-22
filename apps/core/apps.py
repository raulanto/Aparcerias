from django.apps import AppConfig

"""
Configurar cada modulo de apps para que django lo reconoscas


"""

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
