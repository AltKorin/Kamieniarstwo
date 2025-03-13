from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField("Imię", max_length=100)
    last_name = models.CharField("Nazwisko", max_length=100)
    position = models.CharField("Stanowisko", max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"

class Client(models.Model):
    first_name = models.CharField("Imię", max_length=100)
    last_name = models.CharField("Nazwisko", max_length=100)
    phone = models.CharField("Telefon", max_length=20)
    alternative_phone = models.CharField("Alternatywny telefon", max_length=20, blank=True, null=True)
    email = models.EmailField("Email")
    mailing_address = models.CharField("Adres korespondencyjny", max_length=255)
    pesel = models.CharField("PESEL", max_length=11, unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Material(models.Model):
    name = models.CharField("Nazwa materiału", max_length=100)
    price = models.DecimalField("Cena", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    
class OrderTemplate(models.Model):
    TEMPLATE_CHOICES = [
        ('nagrobek', 'Nagrobek'),
        ('oblozenie', 'Obłożenie'),
        ('podniesienie_nagrobka', 'Podniesienie nagrobka'),
        ('dopiska_po_pogrzebie', 'Dopiska po pogrzebie'),
        ('ekshumacja', 'Ekshumacja'),
        ('nowy_szablon', 'Nowy Szablon'),
    ]
    
    name = models.CharField("Nazwa szablonu", max_length=100, choices=TEMPLATE_CHOICES)
    description = models.TextField("Opis", blank=True, null=True)

    def __str__(self):
        return self.get_name_display()

class Order(models.Model):
    
    STATUS_CHOICES = [
        ('wycena', 'Wycena'),
        ('przyjete', 'Przyjęte do realizacji'),
        ('realizacja', 'W realizacji'),
        ('platnosc', 'Czeka na płatność'),
        ('zakonczone', 'Zakończone'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    template = models.ForeignKey(OrderTemplate, on_delete=models.CASCADE, related_name='orders')
    description = models.TextField("Opis", blank=True, null=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='wycena')
    created_at = models.DateTimeField("Data utworzenia", default=timezone.now)
    
    # Nowe pola
    city = models.CharField("Miasto", max_length=100)
    street = models.CharField("Ulica", max_length=100)
    plot = models.CharField("Kwatera", max_length=100)
    grave_type = models.CharField("Typ mogiły", max_length=50, choices=[('ziemna', 'Ziemna'), ('grobowiec', 'Grobowiec')])
    grave_size = models.CharField("Rozmiar grobu", max_length=50, choices=[('pojedynczy', 'Pojedynczy'), ('poltorak', 'Półtorak'), ('podwojny', 'Podwójny')])
    border_material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='border_material')
    frame_material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='frame_material')
    main_plate_material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='main_plate_material')
    lamp = models.BooleanField("Lampion", default=False)
    lamp_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Cena lampy')
    vase = models.BooleanField("Wazon", default=False)
    vase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Cena wazonu')
    ball = models.BooleanField("Kula", default=False)
    ball_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Cena kuli')
    other_accessories = models.TextField("Inne akcesoria", blank=True, null=True)
    other_accessories_price = models.DecimalField("Cena innych akcesoriów", max_digits=10, decimal_places=2, blank=True, null=True)
    inscription = models.TextField("Litery", blank=True, null=True)
    letter_color = models.CharField("Kolor liter", max_length=50, blank=True, null=True)
    font = models.CharField("Czcionka", max_length=50, blank=True, null=True)
    inscription_image = models.ImageField("Zdjęcie z rozkładu treści tablicy", upload_to='inscription_images/', blank=True, null=True)
    covering = models.BooleanField("Obłożenie", default=False)
    covering_material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='covering_material', blank=True)
    covering_quantity = models.DecimalField("Ilość m2", max_digits=10, decimal_places=2, blank=True, null=True)
    covering_cost = models.DecimalField("Koszt obłożenia", max_digits=10, decimal_places=2, blank=True, null=True)
    curbs_quantity = models.DecimalField("Ilość mb krawężnika", max_digits=10, decimal_places=2, blank=True, null=True)
    monument_cost = models.DecimalField("Koszt wykonania", max_digits=10, decimal_places=2, blank=True, null=True)
    old_monument_removal = models.DecimalField("Demontaż starego", max_digits=10, decimal_places=2, blank=True, null=True)
    cemetery_fee = models.DecimalField("Opłata cmentarna", max_digits=10, decimal_places=2, blank=True, null=True)
    transport_cost = models.DecimalField("Koszt transportu", max_digits=10, decimal_places=2, blank=True, null=True)
    other_costs = models.TextField("Koszta inne", blank=True, null=True)
    other_costs_price = models.DecimalField("Koszta inne", max_digits=10, decimal_places=2, blank=True, null=True)
    completion_date = models.DateField("Termin wykonania nagrobka", blank=True, null=True)
    advance_payment = models.DecimalField("Zaliczka", max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField("Metoda płatności", max_length=50, choices=[('card', 'Karta'), ('cash', 'Gotówka'), ('transfer', 'Przelew w ciągu 3 dni')], blank=True, null=True)
    total_cost = models.DecimalField("Suma kosztów", max_digits=10, decimal_places=2, blank=True, null=True)

    def calculate_covering_cost(self):
        if self.covering and self.covering_material and self.covering_quantity:
            return self.covering_material.price * self.covering_quantity + 70
        return 0

    def remaining_payment(self):
        if self.total_cost and self.advance_payment:
            return self.total_cost - self.advance_payment
        return self.total_cost
    
    def progress(self):
        tasks = self.tasks.all()
        if not tasks:
            return 0
        completed = tasks.filter(completed=True).count()
        total = tasks.count()
        return int((completed / total) * 100)
    
    def calculate_total_cost(self):
        total = 0
        if self.lamp and self.lamp_price:
            total += self.lamp_price
        if self.vase and self.vase_price:
            total += self.vase_price
        if self.ball and self.ball_price:
            total += self.ball_price
        if self.covering and self.covering_material and self.covering_quantity:
            total += self.covering_material.price * self.covering_quantity + 70
        if self.other_accessories_price:
            total += self.other_accessories_price
        total += self.monument_cost or 0
        total += self.old_monument_removal or 0
        total += self.cemetery_fee or 0
        total += self.transport_cost or 0
        total += self.other_costs_price or 0
        return total
    
    def calculate_total_paid(self):
        total_paid = self.advance_payment or Decimal('0.00')
        total_paid += sum(payment.amount for payment in Payment.objects.filter(order=self))
        return total_paid
    
    def calculate_remaining_payment(self):
        total_cost = self.total_cost or Decimal('0.00')
        total_paid = self.calculate_total_paid()
        return total_cost - total_paid


    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Zlecenie {self.id} dla {self.client}"
    
    @property
    def total_paid(self):
        return self.calculate_total_paid()

    @property
    def remaining_payment(self):
        return self.calculate_remaining_payment()

class TaskTemplate(models.Model):
    order_template = models.ForeignKey(OrderTemplate, on_delete=models.CASCADE, related_name='task_templates')
    name = models.CharField("Nazwa zadania", max_length=100, unique=True)
    description = models.TextField("Opis zadania", blank=True, null=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    task_template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='tasks')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)  # Zaktualizowane pole
    name = models.CharField(max_length=255)
    description = models.TextField(default='Brak opisu')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField("Zdjęcie", upload_to='task_images/', blank=True, null=True)  # Dodane pole

    def progress(self):
        subtasks = self.subtasks.all()
        if not subtasks:
            return 0
        completed = subtasks.filter(completed=True).count()
        total = subtasks.count()
        return int((completed / total) * 100)
    
    def __str__(self):
        return self.name

class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    name = models.CharField("Nazwa podzadania", max_length=100)
    completed = models.BooleanField("Wykonane", default=False)
    
    def __str__(self):
        return self.name

class Photo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField("Zdjęcie", upload_to='order_photos/')
    uploaded_at = models.DateTimeField("Data dodania", default=timezone.now)
    
    def __str__(self):
        return f"Zdjęcie {self.id} do Zlecenia {self.order.id}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField("Kwota", max_digits=10, decimal_places=2)
    date = models.DateField("Data")
    method = models.CharField("Metoda płatności", max_length=50, choices=[('card', 'Karta'), ('cash', 'Gotówka'), ('transfer', 'Przelew')])

    def __str__(self):
        return f"Płatność {self.id} dla {self.client}"    
