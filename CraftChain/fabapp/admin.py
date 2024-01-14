from django.contrib import admin

# Register your models here.

from .models import CustomerRequirements, Inventory

admin.site.register(CustomerRequirements)
admin.site.register(Inventory)
