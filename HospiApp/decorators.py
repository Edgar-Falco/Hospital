from django.shortcuts import redirect
from functools import wraps

def solo_medico(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'medico'):
            return view_func(request, *args, **kwargs)
        return redirect('no_autorizado')
    return _wrapped_view

def solo_paciente(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'paciente'):
            return view_func(request, *args, **kwargs)
        return redirect('no_autorizado')
    return _wrapped_view

def solo_secretaria(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'secretaria'):
            return view_func(request, *args, **kwargs)
        return redirect('no_autorizado')
    return _wrapped_view
