from django.contrib import admin

# Register your models here.
from .models import Paciente, Medico, Turno, InformeMedico,  Secretaria  

admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Turno)
admin.site.register(InformeMedico)
admin.site.register(Secretaria)