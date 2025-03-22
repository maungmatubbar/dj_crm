from django.contrib import admin
from .models import Client
# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email","phone", "created_at")

admin.site.register(Client, ClientAdmin)
