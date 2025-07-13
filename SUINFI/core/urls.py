from django.urls import path
from . import views

app_name = 'core'  # ¡Esta línea es crucial para el namespace! | Nombre general de la aplicación para todas las URLs

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('users/', views.user_list, name='user_list'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/search/', views.search_services, name='search_services'),
    path('professionals/add/', views.add_professional, name='add_professional'),
    path('professionals/', views.professional_list, name='professional_list'),
    path('professionals/delete/<int:professional_id>/', views.delete_professional, name='delete_professional'),
    path('professionals/edit/<int:professional_id>/', views.edit_professional, name='edit_professional'),
]