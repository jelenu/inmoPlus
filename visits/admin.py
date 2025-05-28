from django.contrib import admin
from .models import Visit

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('property', 'client', 'agent', 'date', 'status')
    search_fields = ('property__title', 'client__name')
    list_filter = ('status', 'agent')
