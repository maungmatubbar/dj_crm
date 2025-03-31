from django.contrib import admin
from .models import Client, Rent, Service, Product, Order
# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email","phone", "created_at")

admin.site.register(Client, ClientAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("client", "amount", "order_date")

admin.site.register(Order, OrderAdmin)    

class RentAdmin(admin.ModelAdmin):
    list_display = ("client", "rent_receive_amount", "receive_date")

admin.site.register(Rent, RentAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("client", "service_name", "amount", "service_date")

admin.site.register(Service, ServiceAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("client", "product_name", "price", "date")

admin.site.register(Product, ProductAdmin)