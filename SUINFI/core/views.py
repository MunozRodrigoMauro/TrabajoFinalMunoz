from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, User
from datetime import datetime
from django.contrib import messages
from .forms import ServiceForm, ServiceSearchForm, ProfessionalForm, Professional, ProfessionalSearchForm
from django.db.models import Q

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
    context={
        'service': service,
        'title': 'Detalles del Servicio',
    }
    return render(request, 'core/service_detail.html', context)

def user_list(request):
    users = User.objects.all() # o Professional.objects.all() según necesidad
    context = {
        'users': users,
        'title': 'Registros',
        'subtitle': 'Usuarios en la plataforma',
      }
    return render(request, 'core/users_list.html', context)
    
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Servicio agregado correctamente.')
            return redirect('core:service_list')
    else:
        form = ServiceForm()
    return render(request, 'core/add_service.html', {'form': form})


def search_services(request):
    form = ServiceSearchForm(request.GET or None)
    services = Service.objects.all()

    if form.is_valid():
        category = form.cleaned_data.get('category')
        if category:
            services = services.filter(category=category)

    context = {
        'form': form,
        'services': services,
        'title': 'Resultados de Búsqueda',
        'subtitle': 'Servicios según categoría',
    }
    return render(request, 'core/search_results.html', context)

def add_professional(request):
    if request.method == 'POST':
        form = ProfessionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:user_list')  # redirige a lista de usuarios después de guardar
    else:
        form = ProfessionalForm()

    return render(request, 'core/add_professional.html', {'form': form})

def professional_list(request):
    professionals = Professional.objects.select_related('user').all()
    context = {
        'professionals': professionals,
        'title': 'Lista de Profesionales',
        'subtitle': 'Conocé a nuestros expertos',
    }
    return render(request, 'core/professional_list.html', context)

def professional_list(request):
    form = ProfessionalSearchForm(request.GET)
    professionals = Professional.objects.select_related('user').all()

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            professionals = professionals.filter(
                Q(user__username__icontains=query) |
                Q(profession__icontains=query)
            )

    context = {
        'form': form,
        'professionals': professionals,
        'title': 'Profesionales disponibles',
        'subtitle': 'Podés buscar por nombre de usuario o profesión',
    }
    return render(request, 'core/professional_list.html', context)

def delete_professional(request, professional_id):
    professional = get_object_or_404(Professional, id=professional_id)
    user = professional.user  # También eliminaremos el usuario relacionado

    if request.method == "POST":
        user.delete()  # Esto también elimina el Professional porque es OneToOne con CASCADE
        messages.success(request, "Profesional eliminado correctamente.")
        return redirect('core:professional_list')

    return render(request, 'core/confirm_delete.html', {'professional': professional})

# core/views.py

def edit_professional(request, professional_id):
    professional = get_object_or_404(Professional, id=professional_id)

    if request.method == 'POST':
        form = ProfessionalForm(request.POST, instance=professional)
        if form.is_valid():
            form.save()
            messages.success(request, "Profesional actualizado correctamente.")
            return redirect('core:professional_list')
    else:
        form = ProfessionalForm(instance=professional)

    return render(request, 'core/edit_professional.html', {
        'form': form,
        'professional': professional,
    })
