from django.contrib import admin

from patient.models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass