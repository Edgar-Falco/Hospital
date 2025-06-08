from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("quienes_somos/", views.quienes_somos, name="quienes_somos"),
    path("personal/", views.personal, name="personal"),
    path("pedir_turno/", views.pedir_turno, name="pedir_turno"),
    path("cargar_informe/<int:turno_id>/", views.cargar_informe, name="cargar_informe"),
    path("login/", views.login_view, name="login"),
    path("turnos_paciente/", views.turnos_paciente, name="turnos_paciente"),
    path("dashboard_medico/", views.turnos_medico, name="dashboard_medico"),
    path("informes/", views.informes_paciente, name="informes_paciente"),
    path("pedir_turno/", views.pedir_turno, name="pedir_turno"),
    path("logout/", views.logout_view, name="logout"),
    path("ver_informe/<int:turno_id>/", views.ver_informe, name="ver_informe"),
    path("ver_informe_medico/<int:turno_id>/", views.ver_informe_medico, name="ver_informe_medico_por_medico"),
    
    path('menu_secre/', views.menu_secre, name='menu_secre'),
    path('pacientes/registrar/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/<int:paciente_id>/editar/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/<int:paciente_id>/eliminar/', views.eliminar_paciente, name='eliminar_paciente'),
    
    path("mis_datos/", views.mis_datos, name="mis_datos"),

    path('chat/', views.chat, name='chat'),
    
    path('no_autorizado/', views.no_autorizado, name='no_autorizado'),


]
