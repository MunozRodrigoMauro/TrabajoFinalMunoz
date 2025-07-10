from django.urls import path
from . import views

app_name = 'core'  # ¡Esta línea es crucial para el namespace!

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('users/', views.user_list, name='user_list'),
]