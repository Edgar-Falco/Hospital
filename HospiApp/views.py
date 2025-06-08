from django.shortcuts import render, redirect, get_object_or_404
from .forms import TurnoForm, InformeMedicoForm,  PacienteCreationForm, PerfilUsuarioForm, CambioPasswordForm
from .models import Turno, InformeMedico , Paciente, Mensaje
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Q
from .decorators import solo_medico, solo_paciente, solo_secretaria




# def inicio(request):
#     return render(request, "HospiApp/inicio.html")


def inicio(request):
    mensajes_no_leidos = 0
    if request.user.is_authenticated:
        mensajes_no_leidos = Mensaje.objects.filter(receptor=request.user, leido=False).count()
    return render(request, "HospiApp/inicio.html", {
        "mensajes_no_leidos": mensajes_no_leidos
    })



def quienes_somos(request):
    return render(request, "HospiApp/quienes_somos.html")

def personal(request):
    return render(request, "HospiApp/personal.html")




#                                             $$$$$ LOGIN y LOGOUT$$$$$$
#Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Redireccion segun el tipo de usuario
            if hasattr(user, "paciente"):
                return redirect("turnos_paciente")  # cambia ala vista de pte
            elif hasattr(user, "medico"):
                return redirect("dashboard_medico")  # cambia a la vista 
            elif hasattr(user, "secretaria"):
                return redirect("menu_secre")  # cambia a la vista de secretaria ultima que agrego!
            else:
                return redirect("inicio")
        else:
            messages.error(request, "Usuario o contraseña incorrectos. Volve a intentarlo salamin")
    
    return render(request, "HospiApp/login.html")

#Logout    
def logout_view(request):
    logout(request)
    return redirect("inicio")





    



#                                                               $$$$$ PACIENTES $$$$$$

# pedir_turno
@login_required
@solo_paciente
def pedir_turno(request):
    if request.method == "POST":
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.paciente = request.user.paciente  # asignar paciente actual
            turno.save()
            return redirect("turnos_paciente")
    else:
        form = TurnoForm()
    return render(request, "HospiApp/pedir_turno.html", {"form": form})


# turnos_paciente
@login_required
@solo_paciente
def turnos_paciente(request):
    turnos = Turno.objects.filter(paciente__user=request.user)
    return render(request, "HospiApp/turnos_paciente.html", {"turnos": turnos})



# ver_informe
@login_required
@solo_paciente
def ver_informe(request, turno_id):
    try:
        informe = InformeMedico.objects.get(turno_id=turno_id)
    except InformeMedico.DoesNotExist:
        informe = None
    return render(request, "HospiApp/ver_informe.html", {"informe": informe})



# informes_paciente
@login_required
@solo_paciente
def informes_paciente(request):
    # Obtener el paciente asociado al usuario actual
    paciente = request.user.paciente
    # Filtrar informes medicos que pertenecen a ese paciente
    informes = InformeMedico.objects.filter(turno__paciente=paciente)
    return render(request, "HospiApp/informes_paciente.html", {"informes": informes})









#                                                               $$$$$ MEDICOS $$$$$$


# turnos_medico

@login_required  # Vista de turnos para medicos con filtro para mayusculas y minúsculas. El medico solo ve sus pacientes
@solo_medico
def turnos_medico(request):
    if hasattr(request.user, "medico"):
        medico = request.user.medico
        query = request.GET.get("q", "")
        
        turnos = Turno.objects.filter(medico=medico).order_by("fecha", "hora")
        
        if query:
            turnos = turnos.filter(
                Q(paciente__user__first_name__icontains=query) |
                Q(paciente__user__last_name__icontains=query)
            )

        return render(request, "HospiApp/turnos_medico.html", {"turnos": turnos, "query": query})
    else:
        return redirect("inicio")  # Redirigir si no es doctor






# cargar_informe
@login_required
@solo_medico
def cargar_informe(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)

    if turno.medico == request.user.medico:
        if request.method == "POST":
            form = InformeMedicoForm(request.POST)
            if form.is_valid():
                informe = form.save(commit=False)
                informe.turno = turno
                informe.save()
                return redirect("dashboard_medico")
        else:
            form = InformeMedicoForm()
        return render(request, "HospiApp/cargar_informe.html", {"form": form, "turno": turno})
    else:
        return redirect("no_autorizado")
    


# ver_informe_medico

@login_required
@solo_medico
def ver_informe_medico(request, turno_id):
    informe = get_object_or_404(InformeMedico, turno__id=turno_id)
    return render(request, "HospiApp/ver_informe_medico_por_medico.html", {"informe": informe})








#                                                               $$$$$ SECRETARIA $$$$$$

@login_required
@solo_secretaria
def menu_secre(request):
    return render(request, "HospiApp/menu_secre.html")



@login_required
@solo_secretaria
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteCreationForm()
    return render(request, 'HospiApp/crear_paciente.html', {'form': form})


@login_required
@solo_secretaria
def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'HospiApp/lista_pacientes.html', {'pacientes': pacientes})


@login_required
@solo_secretaria
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = PacienteCreationForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteCreationForm(instance=paciente)
    return render(request, 'HospiApp/editar_paciente.html', {'form': form})


@login_required
@solo_secretaria
def eliminar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        paciente.user.delete()  # tb borra al usuario
        paciente.delete()
        return redirect('lista_pacientes')
    return render(request, 'HospiApp/eliminar_paciente.html', {'paciente': paciente})

    
    
    

#                          $$$$$$ Mis_datos  y Cambio de pass$$$$$$


@login_required
def mis_datos(request):
    user = request.user
    perfil_form = PerfilUsuarioForm(instance=user)
    password_form = CambioPasswordForm()

    if request.method == 'POST':
        perfil_form = PerfilUsuarioForm(request.POST, instance=user)
        password_form = CambioPasswordForm(request.POST)
        
        if perfil_form.is_valid() and password_form.is_valid():
            perfil_form.save()
            nueva_pass = password_form.cleaned_data['password1']
            user.set_password(nueva_pass)
            user.save()
            messages.success(request, "Datos actualizados correctamente.")
            return redirect('login')  # cuando cambie la contraseña, vuelvo a login

    return render(request, 'HospiApp/mis_datos.html', {
        'perfil_form': perfil_form,
        'password_form': password_form,
        'user': user,
    })
    
    
    
    
    
#                                                               $$$$$ CHAT MENSAJES $$$$$$





@login_required
def chat(request):
    usuarios = User.objects.exclude(id=request.user.id)
    receptor_id = request.GET.get("receptor")
    mensajes = []

    if request.method == "POST":
        contenido = request.POST.get("contenido")
        receptor = get_object_or_404(User, id=request.POST.get("receptor"))
        Mensaje.objects.create(emisor=request.user, receptor=receptor, contenido=contenido)
        return redirect(f'/chat/?receptor={receptor.id}')

    if receptor_id:
        receptor = get_object_or_404(User, id=receptor_id)
        mensajes = Mensaje.objects.filter(            
            (Q(emisor=request.user, receptor=receptor) |
            Q(emisor=receptor, receptor=request.user))
            
        ).order_by("timestamp")

        # ✅ Marcar como leídos los mensajes recibidos
        mensajes.filter(receptor=request.user, leido=False).update(leido=True)

    return render(request, "HospiApp/chat.html", {
        "usuarios": usuarios,
        "receptor_id": receptor_id,
        "mensajes": mensajes,
    })
    


#                           $$$$ Vista de acceesos denegados $$$$$  hago esto aunque ya tenia decoradores/hasattr

def no_autorizado(request):
    return render(request, 'HospiApp/no_autorizado.html')
