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
    border = models.BooleanField("Obwódka", default=False)
    border_material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='border_material')
    border_dimensions = models.CharField("Wymiary obwódki", max_length=100)
    border_price = models.DecimalField("Cena obwódki", max_digits=10, decimal_places=2, blank=True, null=True)
    frame = models.BooleanField("Rama", default=False)
    frame_material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='frame_material')
    frame_height = models.CharField("Wysokość ramy", max_length=100)
    frame_price = models.DecimalField("Cena ramy", max_digits=10, decimal_places=2, blank=True, null=True)
    main_plate = models.BooleanField("Płyta główna", default=False)
    main_plate_material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='main_plate_material')
    main_plate_dimensions = models.CharField("Wymiary płyty głównej", max_length=100)
    main_plate_price = models.DecimalField("Cena płyty głównej", max_digits=10, decimal_places=2, blank=True, null=True)
    lamp = models.BooleanField("Lampion", default=False)
    lamp_price = models.DecimalField("Cena lampionu", max_digits=10, decimal_places=2, blank=True, null=True)
    vase = models.BooleanField("Wazon", default=False)
    vase_price = models.DecimalField("Cena wazonu", max_digits=10, decimal_places=2, blank=True, null=True)
    ball = models.BooleanField("Kula", default=False)
    ball_price = models.DecimalField("Cena kuli", max_digits=10, decimal_places=2, blank=True, null=True)
    other_accessories = models.TextField("Inne akcesoria", blank=True, null=True)
    inscription = models.TextField("Litery", blank=True, null=True)
    letter_color = models.CharField("Kolor liter", max_length=50, blank=True, null=True)
    font = models.CharField("Czcionka", max_length=50, blank=True, null=True)
    inscription_image = models.ImageField("Zdjęcie z rozkładu treści tablicy", upload_to='inscription_images/', blank=True, null=True)
    covering = models.BooleanField("Obłożenie", default=False)
    covering_price = models.DecimalField("Cena m2", max_digits=10, decimal_places=2, blank=True, null=True)
    covering_quantity = models.DecimalField("Ilość m2", max_digits=10, decimal_places=2, blank=True, null=True)
    curbs_price = models.DecimalField("Cena mb", max_digits=10, decimal_places=2, blank=True, null=True)
    curbs_quantity = models.DecimalField("Ilość mb", max_digits=10, decimal_places=2, blank=True, null=True)
    monument_cost = models.DecimalField("Koszt wykonania", max_digits=10, decimal_places=2, blank=True, null=True)
    old_monument_removal = models.DecimalField("Demontaż starego", max_digits=10, decimal_places=2, blank=True, null=True)
    cemetery_fee = models.DecimalField("Opłata cmentarna", max_digits=10, decimal_places=2, blank=True, null=True)
    transport_cost = models.DecimalField("Koszt transportu", max_digits=10, decimal_places=2, blank=True, null=True)
    other_costs = models.TextField("Koszta inne", blank=True, null=True)
    total_cost = models.DecimalField("Suma kosztów", max_digits=10, decimal_places=2, blank=True, null=True)
    completion_date = models.DateField("Termin wykonania nagrobka", blank=True, null=True)
    advance_payment = models.DecimalField("Zaliczka", max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField("Metoda płatności", max_length=50, choices=[('card', 'Karta'), ('cash', 'Gotówka'), ('transfer', 'Przelew w ciągu 3 dni')], blank=True, null=True)
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
    
    def __str__(self):
        return f"Zlecenie {self.id} dla {self.client}"

class TaskTemplate(models.Model):
    order_template = models.ForeignKey(OrderTemplate, on_delete=models.CASCADE, related_name='task_templates')
    name = models.CharField("Nazwa zadania", max_length=100)
    description = models.TextField("Opis zadania", blank=True, null=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1)  # Zakładając, że istnieje zlecenie o ID 1
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
