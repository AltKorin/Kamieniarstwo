from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import EmployeeEditForm, SignUpForm, OrderForm, ShortOrderForm, TaskForm, SubTaskForm, PaymentForm
from .models import Order, Task, SubTask, Photo, Client, Payment, Employee, TaskTemplate
from django.contrib.auth import views as auth_views
from django.db import IntegrityError
from decimal import Decimal, InvalidOperation
from .forms import ClientCreationForm
from .forms import TaskTemplateForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Ustaw is_staff na True, aby oznaczyć użytkownika jako pracownika
            user.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            position = form.cleaned_data.get('position')
            if not Employee.objects.filter(user=user).exists():
                Employee.objects.create(user=user, first_name=first_name, last_name=last_name, position=position)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'orders/signup.html', {'form': form})

def login_view(request):
    return auth_views.LoginView.as_view(template_name='orders/login.html')(request)

def logout_view(request):
    logout(request)
    return redirect('home')

def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            client = Client.objects.get(user=request.user)
            order.client = client
            order.save()
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'orders/add_order.html', {'form': form})

def home(request):
    return render(request, 'orders/home.html')

@login_required
def dashboard(request):
    orders = Order.objects.all()
    clients = Client.objects.all()
    payments = Payment.objects.all()
    tasks = Task.objects.all()
    employees = Employee.objects.all()
    return render(request, 'orders/dashboard.html', {
        'orders': orders,
        'clients': clients,
        'tasks': tasks,
        'payments': payments,
        'employees': employees,
    })

@login_required
def clients(request):
    clients = Client.objects.all()
    return render(request, 'orders/clients.html', {'clients': clients})

@login_required
def orders(request):
    orders = Order.objects.all()
    return render(request, 'orders/orders.html', {'orders': orders})

@login_required
def payments(request):
    payments = Order.objects.filter(status='platnosc')
    return render(request, 'orders/payments.html', {'payments': payments})

@login_required
def archive(request):
    archived_orders = Order.objects.filter(status='zakonczone')
    return render(request, 'orders/archive.html', {'archived_orders': archived_orders})

@login_required
def reports(request):
    reports = Order.objects.all()  # Możesz dostosować filtrowanie raportów według potrzeb
    return render(request, 'orders/reports.html', {'reports': reports})

def view_order(request, order_id):
    order = Order.objects.get(id=order_id)
    tasks = order.tasks.all()
    photos = order.photos.all()
    return render(request, 'orders/view_order.html', {'order': order, 'tasks': tasks, 'photos': photos})

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_cost = calculate_total_cost(order)  # Oblicz total_cost
            order.save()
            return redirect('dashboard')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/edit_order.html', {'form': form, 'booleanFields': ['border', 'frame', 'main_plate', 'lamp', 'vase', 'ball', 'covering']})

def calculate_total_cost(order):
    # Oblicz total_cost na podstawie pól zamówienia
    total_cost = Decimal('0.00')
    price_fields = ['border_price', 'frame_price', 'main_plate_price', 'lamp_price', 'vase_price', 'ball_price', 'covering_price', 'curbs_price', 'monument_cost', 'old_monument_removal', 'cemetery_fee', 'transport_cost', 'other_costs']
    for field in price_fields:
        value = getattr(order, field, 0)
        if value:
            try:
                total_cost += Decimal(value)
            except InvalidOperation:
                pass  # Ignoruj wartości, które nie mogą być przekonwertowane na Decimal
    return total_cost

def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')
    return render(request, 'orders/delete_order.html', {'order': order})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'orders/task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('view_task', task_id=task.id)
    else:
        form = TaskForm()
    return render(request, 'orders/create_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('view_task', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'orders/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'orders/delete_task.html', {'task': task})

@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    subtasks = task.subtasks.all()
    return render(request, 'orders/view_task.html', {'task': task, 'subtasks': subtasks})

@login_required
def create_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.task = task
            subtask.save()
            return redirect('view_task', task_id=task.id)
    else:
        form = SubTaskForm()
    return render(request, 'orders/create_subtask.html', {'form': form, 'task': task})

@login_required
def edit_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect('view_task', task_id=subtask.task.id)
    else:
        form = SubTaskForm(instance=subtask)
    return render(request, 'orders/edit_subtask.html', {'form': form, 'subtask': subtask})

@login_required
def create_client(request):
    if request.method == 'POST':
        form = ClientCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClientCreationForm()
    return render(request, 'orders/create_client.html', {'form': form})

@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientCreationForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ClientCreationForm(instance=client)
    return render(request, 'orders/edit_client.html', {'form': form})

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('dashboard')
    return render(request, 'orders/delete_client.html', {'client': client})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, Task, TaskTemplate

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            # Dodaj zadania na podstawie wybranego szablonu
            template = order.template
            task_templates = TaskTemplate.objects.filter(order_template=template)
            for task_template in task_templates:
                Task.objects.create(
                    order=order,
                    name=task_template.name,
                    description=task_template.description
                )
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form})

@login_required
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'orders/edit_payment.html', {'form': form})
@login_required
def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        payment.delete()
        return redirect('dashboard')
    return render(request, 'orders/delete_payment.html', {'payment': payment})

@login_required
def employees(request):
    employees = Employee.objects.all()
    return render(request, 'orders/employees.html', {'employees': employees})

@login_required
def employee_tasks(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    tasks = Task.objects.filter(assigned_to=employee.user)
    return render(request, 'orders/employee_tasks.html', {'employee': employee, 'tasks': tasks})

@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeEditForm(request.POST, instance=employee.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            employee.first_name = form.cleaned_data.get('first_name')
            employee.last_name = form.cleaned_data.get('last_name')
            employee.position = form.cleaned_data.get('position')
            employee.save()
            return redirect('dashboard')
    else:
        form = EmployeeEditForm(instance=employee.user)
    return render(request, 'orders/edit_employee.html', {'form': form, 'employee': employee})

@login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        user = employee.user
        employee.delete()
        user.delete()
        return redirect('dashboard')
    return render(request, 'orders/delete_employee.html', {'employee': employee})

@login_required
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'orders/payment_list.html', {'payments': payments})

@login_required
def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'orders/payment_form.html', {'form': form})

@login_required
def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'orders/payment_form.html', {'form': form})

from .forms import TaskTemplateForm
from .models import TaskTemplate

def add_task_template(request):
    if request.method == 'POST':
        form = TaskTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_template_list')
    else:
        form = TaskTemplateForm()
    return render(request, 'orders/add_task_template.html', {'form': form})

def task_template_list(request):
    if request.method == 'POST':
        form = TaskTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_template_list')
    else:
        form = TaskTemplateForm()
    
    task_templates = TaskTemplate.objects.all()
    return render(request, 'orders/task_template_list.html', {'task_templates': task_templates, 'form': form})

def add_task(request, template_id):
    task_template = get_object_or_404(TaskTemplate, id=template_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_template = task_template
            task.save()
            return redirect('task_template_list')
    else:
        form = TaskForm(initial={'task_template': task_template})
    return render(request, 'orders/add_task.html', {'form': form, 'task_template': task_template})

