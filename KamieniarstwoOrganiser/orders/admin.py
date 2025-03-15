from django.contrib import admin
from .models import Client, Order, Task, Photo

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Task)
admin.site.register(Photo)