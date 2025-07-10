from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Client, Professional, Service, Contract, PaymentMethod

# Customización básica del User para el admin
class UserAdmin(BaseUserAdmin):
    # Campos que aparecen en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

# Registrar todos los modelos
admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(Professional)
admin.site.register(Service)
admin.site.register(Contract)
admin.site.register(PaymentMethod)