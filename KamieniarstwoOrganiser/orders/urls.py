from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('create_client/', views.create_client, name='create_client'),
    path('create_order/', views.create_order, name='create_order'),
    path('create_task/', views.create_task, name='create_task'),
    path('clients/', views.clients, name='clients'),
    path('orders/', views.orders, name='orders'),
    path('payments/', views.payment_list, name='payment_list'),  # Dodano ścieżkę URL dla listy płatności
    path('payments/create/', views.create_payment, name='create_payment'),
    path('payments/edit/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('archive/', views.archive, name='archive'),
    path('reports/', views.reports, name='reports'),
    path('employees/', views.employees, name='employees'),
    path('employee_tasks/<int:employee_id>/', views.employee_tasks, name='employee_tasks'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('view_order/<int:order_id>/', views.view_order, name='view_order'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('view_task/<int:task_id>/', views.view_task, name='view_task'),
    path('create_subtask/<int:task_id>/', views.create_subtask, name='create_subtask'),
    path('edit_subtask/<int:subtask_id>/', views.edit_subtask, name='edit_subtask'),
    path('delete_subtask/<int:subtask_id>/', views.delete_task, name='delete_subtask'),  # Zmieniono na delete_task
    path('edit_client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('employees/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),  # Dodano ścieżkę URL dla edytowania pracownika
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),  # Dodano ścieżkę URL dla usuwania pracownika
    path('add_task_template/', views.add_task_template, name='add_task_template'),
    path('task_template_list/', views.task_template_list, name='task_template_list'),
    path('add_task/<int:template_id>/', views.add_task, name='add_task'),
]