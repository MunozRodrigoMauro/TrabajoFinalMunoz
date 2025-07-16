################################  CBV  ################################
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    index, service_detail, user_list, perfil, editar_user,
    ServiceListView, ServiceCreateView, ServiceSearchView,
    ProfessionalListView, ProfessionalCreateView,
    ProfessionalUpdateView, ProfessionalDeleteView
)

app_name = 'core'  # Namespace de la aplicación para las URLs

urlpatterns = [
    path('', index, name='index'),  # Vista simple FBV
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/<int:service_id>/', service_detail, name='service_detail'),  # Vista simple FBV
    path('users/', user_list, name='user_list'),  # Vista simple FBV
    path('services/add/', ServiceCreateView.as_view(), name='add_service'),
    path('services/search/', ServiceSearchView.as_view(), name='search_services'),
    path('professionals/add/', ProfessionalCreateView.as_view(), name='add_professional'),
    path('professionals/', ProfessionalListView.as_view(), name='professional_list'),
    path('professionals/edit/<int:pk>/', ProfessionalUpdateView.as_view(), name='edit_professional'),
    path('professionals/delete/<int:pk>/', ProfessionalDeleteView.as_view(), name='delete_professional'),
    path('perfil/', perfil, name='perfil'),
    path('editar_perfil/', editar_user, name='editar_perfil'),
]

#Para servir los archivos de medios durante el desarrollo.
if settings.DEBUG: # hacemos esta validación para que servir los estaticos desde django solo en desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
