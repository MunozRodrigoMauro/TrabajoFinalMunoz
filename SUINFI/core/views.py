from django.shortcuts import render, get_object_or_404
from .models import Service, User
from datetime import datetime

def index(request):
    context = {
        'titulo': 'Bienvenido a SUINFI',
        'mensaje': 'Conectamos usuarios con profesionales 👨‍🔧',
    }
    return render(request, 'core/index.html', context)

def service_list(request):
    services = Service.objects.all()
    context = {
        'services': services,
        'title': 'Explorá nuestros Servicios',
        'subtitle': 'Encontrá profesionales para lo que necesitás',
    }
    return render(request, 'core/services_list.html', context)

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'core/service_detail.html', {'service': service})

def user_list(request):
    users = User.objects.all() # o Professional.objects.all() según necesidad
    context = {
        'users': users,
        'title': 'Usuarios Registrados',
        'subtitle': 'Usuarios en la plataforma',
      }
    return render(request, 'core/users_list.html', context)

