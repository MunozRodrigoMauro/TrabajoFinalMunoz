from django.contrib.auth.models import AbstractUser, User
from django.db import models

# -------------------- USER --------------------
class User(AbstractUser):
    # Campo JSON para almacenar dirección completa
    address = models.JSONField(null=True, blank=True)  # Ej: {"street": "...", "city": "...", "country": "..."}
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, default='unspecified')
    birthdate = models.DateField(null=True, blank=True)

    # Métodos de ejemplo que podrían expandirse luego
    def login(self):
        # Aquí puedo implementar logs o control de accesos personalizados
        pass

    def update_data(self, **kwargs):
        # Permite actualizar cualquier dato del usuario
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

    def logout(self):
        # Aquí puedo registrar eventos de cierre de sesión
        pass
    
# -------------------- Payment --------------------
class PaymentMethod(models.Model):

    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('mercado_pago', 'Mercado Pago'),
    ]
    name = models.CharField(max_length=50, choices=METHOD_CHOICES, unique=True)

    def __str__(self):
        return dict(self.METHOD_CHOICES).get(self.name, self.name)

# -------------------- CLIENT --------------------
class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    payment_methods = models.ManyToManyField(PaymentMethod, blank=True)  # Lista de métodos de pago
    contract_history = models.JSONField(default=list)  # Historial de contratos

    def __str__(self):
        return self.user.username


# -------------------- SERVICE --------------------
class Service(models.Model):
     
    CATEGORY_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('electricity', 'Electricity'),
        ('cleaning', 'Cleaning'),
        ('gardening', 'Gardening'),
        ('technology', 'Technology'),
        ('construction', 'Construction'),
        ('carpentry', 'Carpentry'),
        ('painting', 'Painting'),
        ('security', 'Security'),
        ('transport', 'Transport & Moving'),
        ('mechanics', 'Mechanics & Auto Services'),
        ('healthcare', 'Healthcare'),
        ('beauty', 'Beauty & Personal Care'),
        ('pets', 'Pet Services'),
        ('events', 'Events & Entertainment'),
        ('education', 'Education & Tutoring'),
        ('it_support', 'IT Support & Networking'),
        ('legal', 'Legal Services'),
        ('finance', 'Finance & Accounting'),
        ('maintenance', 'General Maintenance'),
        ('appliances', 'Appliance Repair'),
        ('real_estate', 'Real Estate Services'),
        ('marketing', 'Marketing & Advertising'),
        ('writing', 'Writing & Translation'),
        ('coaching', 'Coaching & Mentoring'),
        ('home_decor', 'Home Decor & Interior Design'),
        ('freelance', 'Freelance & Remote Work'),
        ('other', 'Other'),
]

     
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def update_price(self, new_price):
        self.price_per_hour = new_price
        self.save()

    def __str__(self):
        return f"{self.name} - {self.category}"


# -------------------- PROFESSIONAL --------------------
class Professional(models.Model):

    PROFESSION_CHOICES = [
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('cleaner', 'Cleaner'),
        ('gardener', 'Gardener'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('mechanic', 'Mechanic'),
        ('painter', 'Painter'),
        ('mason', 'Mason'),
        ('carpenter', 'Carpenter'),
        ('locksmith', 'Locksmith'),
        ('hvac_technician', 'HVAC Technician'),
        ('welder', 'Welder'),
        ('nurse', 'Nurse'),
        ('chef', 'Chef'),
        ('dog_walker', 'Dog Walker'),
        ('babysitter', 'Babysitter'),
        ('personal_trainer', 'Personal Trainer'),
        ('tutor', 'Tutor'),
        ('translator', 'Translator'),
        ('event_planner', 'Event Planner'),
        ('photographer', 'Photographer'),
        ('videographer', 'Videographer'),
        ('it_support', 'IT Support'),
        ('roofing_specialist', 'Roofing Specialist'),
        ('pest_control', 'Pest Control'),
        ('interior_designer', 'Interior Designer'),
        ('landscaper', 'Landscaper'),
        ('barber', 'Barber'),
        ('makeup_artist', 'Makeup Artist'),
        ('other', 'Other'),
    ]


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='professional_profile'
    )
    profession = models.CharField(max_length=100, choices=PROFESSION_CHOICES, default='other', unique=True)    
    is_verified = models.BooleanField(default=False)
    services = models.ManyToManyField(Service, related_name='professionals', blank=True)

    def add_service(self, service):
        self.services.add(service)

    def list_services(self):
        return self.services.all()

    def __str__(self):
        return f"{self.user.username} - {self.profession}"

# -------------------- CONTRACT --------------------
class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contracts')
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='contracts')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='contracts')

    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )

    def purchase_service(self):
        # Simula la compra cambiando el estado
        self.status = 'in_progress'
        self.save()

    def add_comment(self):
        # Este método puede ser extendido para manejar feedback
        pass

    def __str__(self):
        return f"{self.client.user.username} → {self.professional.user.username} ({self.service.name})"
    
# -------------------- Avatar --------------------
class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    image = models.ImageField(upload_to='avatares', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.image}"
