from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.shortcuts import redirect

from django.contrib.sessions.models import Session

def logout_all_users(request):
    #Session.objects.all().delete()
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de inicio de sesión