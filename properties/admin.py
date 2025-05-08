from django.contrib import admin
from .models import Property, PropertyImage

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "address")

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("property", "uploaded_at")
