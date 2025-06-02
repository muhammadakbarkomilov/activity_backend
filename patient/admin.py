from django.contrib import admin
from .models import PatientData

@admin.register(PatientData)
class PatientDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'date_of_birth')
    search_fields = ('full_name',)

# Register your models here.
