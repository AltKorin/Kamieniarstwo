from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User  # Import domyślnego modelu użytkownika
from .models import Order, Client, Task, Payment, Employee, Material, OrderTemplate

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, label='Nazwa użytkownika')
    email = forms.EmailField(max_length=254, label='Email', help_text='Wymagane. Podaj prawidłowy adres email.')
    first_name = forms.CharField(max_length=100, label='Imię')
    last_name = forms.CharField(max_length=100, label='Nazwisko')
    position = forms.CharField(max_length=100, label='Stanowisko')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Potwierdź hasło')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'position')

class EmployeeEditForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło', required=False)
    position = forms.CharField(max_length=100, label='Stanowisko')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'position')

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'price']

class MaterialSelectWidget(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if value:
            # Jeśli value jest instancją ModelChoiceIteratorValue, pobierz jej właściwą wartość
            pk = value.value if hasattr(value, 'value') else value
            try:
                material = Material.objects.get(pk=pk)
                option['attrs']['data-price'] = str(material.price)
            except Material.DoesNotExist:
                option['attrs']['data-price'] = '0'
        return option

class OrderForm(forms.ModelForm):
    completion_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label='Termin wykonania nagrobka')

    class Meta:
        model = Order
        fields = [
            'client', 'template', 'description', 'status', 'city', 'street', 'plot',
            'grave_type', 'grave_size', 'border_material',
            'frame_material', 'main_plate_material',
            'lamp', 'lamp_price', 'vase', 'vase_price', 'ball', 'ball_price', 'other_accessories', 'other_accessories_price',
            'inscription', 'letter_color', 'font', 'inscription_image', 'covering', 'covering_material', 'covering_quantity',
            'curbs_quantity', 'monument_cost', 'old_monument_removal',
            'cemetery_fee', 'transport_cost', 'other_costs', 'other_costs_price', 'completion_date', 'advance_payment', 'payment_method'
        ]
        labels = {
            'client': 'Klient',
            'template': 'Szablon zlecenia',
            'description': 'Opis',
            'status': 'Status',
            'city': 'Miasto',
            'street': 'Ulica',
            'plot': 'Kwatera',
            'grave_type': 'Typ mogiły',
            'grave_size': 'Rozmiar grobu',
            'border_material': 'Materiał obwódki',
            'border_dimensions': 'Wymiary obwódki',
            'frame_material': 'Materiał ramy',
            'frame_height': 'Wysokość ramy',
            'main_plate_material': 'Materiał płyty głównej',
            'main_plate_dimensions': 'Wymiary płyty głównej',
            'lamp': 'Lampion',
            'lamp_price': 'Cena lampionu',
            'vase': 'Wazon',
            'vase_price': 'Cena wazonu',
            'ball': 'Kula',
            'ball_price': 'Cena kuli',
            'other_accessories': 'Inne akcesoria',
            'inscription': 'Litery',
            'letter_color': 'Kolor liter',
            'font': 'Czcionka',
            'inscription_image': 'Zdjęcie z rozkładu treści tablicy',
            'covering': 'Obłożenie',
            'covering_material': 'Materiał obłożenia',
            'covering_quantity': 'Ilość m2',
            'curbs_quantity': 'Ilość mb krawężnika',
            'monument_cost': 'Koszt wykonania nagrobka',
            'old_monument_removal': 'Demontaż starego nagrobka',
            'cemetery_fee': 'Opłata cmentarna',
            'transport_cost': 'Koszt transportu',
            'other_costs': 'Koszta inne',
            'total_cost': 'Suma kosztów',
            'completion_date': 'Termin wykonania nagrobka',
            'advance_payment': 'Zaliczka',
            'payment_method': 'Metoda płatności',
        }
        widgets = {
            'grave_type': forms.Select(choices=[('ziemna', 'Ziemna'), ('grobowiec', 'Grobowiec')]),
            'grave_size': forms.Select(choices=[('pojedynczy', 'Pojedynczy'), ('poltorak', 'Półtorak'), ('podwojny', 'Podwójny')]),
            'covering_material': MaterialSelectWidget(),
        }

class ShortOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['description', 'status']

class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone', 'alternative_phone', 'email', 'mailing_address', 'pesel']
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'phone': 'Telefon',
            'alternative_phone': 'Alternatywny telefon',
            'email': 'Email',
            'mailing_address': 'Adres korespondencyjny',
            'pesel': 'PESEL',
        }
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone', 'alternative_phone', 'email', 'mailing_address', 'pesel']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['order', 'order_template', 'name', 'description', 'assigned_to', 'completed', 'image']
        labels = {
            'order': 'Zlecenie',
            'order_template': 'Szablon zlecenia',
            'name': 'Nazwa zadania',
            'description': 'Opis',
            'assigned_to': 'Przypisany pracownik',
            'completed': 'Zakończone',
            'image': 'Zdjęcie'
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['order', 'amount', 'client', 'date', 'method']
        labels = {
            'order': 'Zlecenie',
            'amount': 'Kwota',
            'client': 'Klient',
            'date': 'Data',
            'method': 'Metoda płatności',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class OrderTemplateForm(forms.ModelForm):
    custom_name = forms.CharField(required=False, label="Nazwa własna")

    class Meta:
        model = OrderTemplate
        fields = ['name', 'custom_name', 'description']
        labels = {
            'name': 'Wybierz szablon',
            'description': 'Opis',
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        custom_name = cleaned_data.get('custom_name')

        if name == 'nowy_szablon':
            if not custom_name:
                raise forms.ValidationError("Podaj nazwę własną dla nowego szablonu.")
            # Ustawiamy pole name na wartość wpisaną w custom_name
            cleaned_data['name'] = custom_name
        return cleaned_data

class TemplateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']
        labels = {
            'name': 'Nazwa zadania',
            'description': 'Opis zadania',
        }