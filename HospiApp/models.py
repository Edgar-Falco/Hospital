from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    


class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.especialidad}"




class Turno(models.Model):
    paciente = models.ForeignKey("Paciente", on_delete=models.CASCADE)
    medico = models.ForeignKey("Medico", on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    

    def __str__(self):
        return f"{self.fecha} - {self.hora} | {self.paciente} con {self.medico}"
    

class InformeMedico(models.Model):
    turno = models.OneToOneField("Turno", on_delete=models.CASCADE)
    diagnostico = models.TextField()
    receta = models.TextField(blank=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Informe del {self.fecha} para {self.turno.paciente}"
    
    
    
class Secretaria(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Secretaria: {self.user.first_name} {self.user.last_name}"
    


class Mensaje(models.Model):
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.emisor} a {self.receptor} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
 