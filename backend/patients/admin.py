from django.contrib import admin
from .models import Patient, PatientState, Entity, Inventory

admin.site.register(Patient)
admin.site.register(PatientState)
admin.site.register(Entity)
admin.site.register(Inventory)
