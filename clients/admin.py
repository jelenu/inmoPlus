from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'agent')
    search_fields = ('name', 'email')
    list_filter = ('agent',)

# Register your models here.
