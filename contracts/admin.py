from django.contrib import admin
from .models import Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('property', 'client', 'agent', 'type', 'status', 'start_date', 'end_date')
    search_fields = ('property__title', 'client__name')
    list_filter = ('type', 'status', 'agent')

# Register your models here.
