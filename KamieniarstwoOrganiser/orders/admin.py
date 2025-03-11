from django.contrib import admin
from .models import Client, Order, Task, TaskTemplate, Photo

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Task)
admin.site.register(TaskTemplate)
admin.site.register(Photo)