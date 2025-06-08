from django import forms
from .models import Turno, InformeMedico,  Paciente
from django.contrib.auth.models import User



class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ["medico", "fecha", "hora"]

class InformeMedicoForm(forms.ModelForm):
    class Meta:
        model = InformeMedico
        fields = ["diagnostico", "receta"]



class PacienteCreationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")

    class Meta:
        model = Paciente
        fields = ['dni', 'telefono']

    def save(self, commit=True):
        # Creacion del usuario
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        paciente = super().save(commit=False)
        paciente.user = user
        if commit:
            paciente.save()
        return paciente



#Mis datos
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Cambio de contraseña y verificacion
class CambioPasswordForm(forms.Form):
    password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
