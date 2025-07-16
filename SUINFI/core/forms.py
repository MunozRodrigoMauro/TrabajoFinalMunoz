from django import forms
from .models import Service, Professional, Avatar
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'price_per_hour']

    def clean_price_per_hour(self):
        price = self.cleaned_data.get('price_per_hour')
        if price < 100:
            raise forms.ValidationError("El precio mínimo debe ser de $100.")
        return price


class ServiceSearchForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'Seleccioná una categoría')] + Service.CATEGORY_CHOICES,
        required=False,
        label='Filtrar por categoría'
    )

class ProfessionalForm(forms.ModelForm):
    class Meta:
        model = Professional  # Modelo sobre el cual se construye el formulario
        fields = ['user', 'profession', 'is_verified', 'services']

        #Este widget es para que los servicios aparezcan como checkboxes
        widgets = {
            'services': forms.CheckboxSelectMultiple(),
        }

    # Esta función es opcional, sirve para agregar validaciones personalizadas
    def clean(self):
        cleaned_data = super().clean()
        services = cleaned_data.get('services')

        if not services:
            self.add_error('services', 'Debes seleccionar al menos un servicio.')

        return cleaned_data
    
class ProfessionalSearchForm(forms.Form):
    query = forms.CharField(label='Buscar profesional', max_length=100, required=False)
    
class EditUserForm(UserChangeForm):
    email = forms.EmailField(required=True,label='Email')
    first_name = forms.CharField
    
class EditUserForm(UserChangeForm):
    email = forms.EmailField(required=True,label='Email')
    first_name = forms.CharField(required=True,label='Nombre')
    last_name = forms.CharField(required=True,label='Apellido')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','password')

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']