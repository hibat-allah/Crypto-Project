from django.contrib import admin
from .models import adv,ps

class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(adv, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(ps, PatientAdmin)