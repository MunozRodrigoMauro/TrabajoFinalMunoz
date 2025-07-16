from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Service, User, Professional, Avatar
from .forms import (
    ServiceForm,
    ServiceSearchForm,
    ProfessionalForm,
    ProfessionalSearchForm,
    EditUserForm,
    AvatarForm
)


# Vista de inicio
def index(request):
    context = {
        'titulo': 'Bienvenido a SUINFI',
        'mensaje': 'Conectamos usuarios con profesionales 👨‍🔧',
    }
    return render(request, 'core/index.html', context)

def perfil(request):
    return render(request, 'core/perfil.html')

@login_required # con este decorador exigimos que el usuario esté logueado para utilizar esta view
def editar_user(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)

        #verificar si el usuario tiene avatar
        try:
            avatar = request.user.avatar
        except Avatar.DoesNotExist:
            avatar = None

        #Crear el formulario de avatar segun si el usuario tiene avatar o no
        if avatar:
            avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        else:
            avatar_form = AvatarForm(request.POST, request.FILES)

        if form.is_valid() and avatar_form.is_valid():
            form.save()
            avatar_instance = avatar_form.save(commit=False)
            avatar_instance.user = request.user
            avatar_instance.save()
            messages.success(request, '✅ Datos del usuario actualizados correctamente.')
            return redirect('core:perfil')
    else:
        form = EditUserForm(instance=request.user)
        if hasattr(request.user, 'avatar'):
            avatar_form = AvatarForm(instance=request.user.avatar)
        else:
            avatar_form = AvatarForm()
    return render(request, 'core/editar_perfil.html', {'form': form, 'avatar_form': avatar_form})

# Detalle de un servicio
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    context = {
        'service': service,
        'title': 'Detalles del Servicio',
    }
    return render(request, 'core/service_detail.html', context)


# Lista de todos los usuarios
def user_list(request):
    users = User.objects.all()
    context = {
        'users': users,
        'title': 'Registros',
        'subtitle': 'Usuarios en la plataforma',
    }
    return render(request, 'core/users_list.html', context)


# Lista de servicios
class ServiceListView(ListView):
    model = Service
    template_name = 'core/services_list.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Explorá nuestros Servicios'
        context['subtitle'] = 'Encontrá profesionales para lo que necesitás'
        return context


# Crear nuevo servicio
class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'core/add_service.html'
    success_url = reverse_lazy('core:service_list')

    def form_valid(self, form):
        messages.success(self.request, '✅ Servicio agregado correctamente.')
        return super().form_valid(form)


# Buscar servicios por categoría
class ServiceSearchView(ListView):
    model = Service
    template_name = 'core/search_results.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = Service.objects.all()
        form = self.get_form()
        if form.is_valid():
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
        return queryset

    def get_form(self):
        return ServiceSearchForm(self.request.GET or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['title'] = 'Resultados de Búsqueda'
        context['subtitle'] = 'Servicios según categoría'
        return context


# Lista de profesionales con filtro por nombre o profesión
class ProfessionalListView(ListView):
    model = Professional
    template_name = 'core/professional_list.html'
    context_object_name = 'professionals'

    def get_queryset(self):
        queryset = Professional.objects.select_related('user').all()
        form = self.get_form()
        if form.is_valid():
            query = form.cleaned_data.get('query')
            if query:
                queryset = queryset.filter(
                    Q(user__username__icontains=query) |
                    Q(profession__icontains=query)
                )
        return queryset

    def get_form(self):
        return ProfessionalSearchForm(self.request.GET or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['title'] = 'Profesionales disponibles'
        context['subtitle'] = 'Podés buscar por nombre de usuario o profesión'
        return context


# Agregar profesional
class ProfessionalCreateView(CreateView):
    model = Professional
    form_class = ProfessionalForm
    template_name = 'core/add_professional.html'
    success_url = reverse_lazy('core:user_list')


# Editar profesional
class ProfessionalUpdateView(UpdateView):
    model = Professional
    form_class = ProfessionalForm
    template_name = 'core/edit_professional.html'
    success_url = reverse_lazy('core:professional_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['professional'] = self.object
        return context


# Eliminar profesional
class ProfessionalDeleteView(DeleteView):
    model = Professional
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('core:professional_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Profesional eliminado correctamente.")
        return super().delete(request, *args, **kwargs)

