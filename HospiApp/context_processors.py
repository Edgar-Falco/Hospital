

#creo este archivo porque el contador porque la variable mensajes_no_leidos no se esta pasando a base_usuarios_inicio.html
#el contador solo se envia a inicio.html y no a todas las vistas que usan base_usuarios_inicio.html
#esto es un archivo donde defino variables globales para que esten disponibles en todas las plantillas, sin tener que pasarlas a mano desde cada vista

#RECORDOR QUE ESTASS COSAS HAY QUE AGREGARLAS EN SETTINGS.PY EN TEMPLATES /CONTEXT_PROCESSORS

from .models import Mensaje
from django.contrib.auth.models import User
from django.db.models import Count


def mensajes_no_leidos(request):
    if request.user.is_authenticated:
        # msj no leidos
        mensajes = Mensaje.objects.filter(receptor=request.user, leido=False)

        # total
        total_no_leidos = mensajes.count()

        # usuarios que enviaron mensajes no leidos
        emisores = (
            mensajes
            .values('emisor__username')
            .annotate(cantidad=Count('id'))
            .order_by('-cantidad')
        )

        nombres_emisores = [e['emisor__username'] for e in emisores]

        return {
            'mensajes_no_leidos': total_no_leidos,
            'emisores_con_mensajes': nombres_emisores
        }
    return {}


