from django.contrib import admin
from .models import Patient, PatientState

admin.site.register(Patient)
admin.site.register(PatientState)
