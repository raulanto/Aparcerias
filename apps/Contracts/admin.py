from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'sharecropper',
        'company',
        'start_date',
        'end_date',
        'status',
    )
    list_filter = ('status', 'company')
    search_fields = ('sharecropper__legal_name', 'crop_or_activity')
