from django.db import models

# Create your models here.
class Client(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"{self.full_name} {self.email} {self.created_at}")
          
# model for rent
class Rent(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    rent_receive_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receive_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Rent paid by {self.client.full_name} {self.receive_date}")
    
#Model for service
class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='service')
    service_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    service_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Service for {self.client.full_name} {self.amount}")

# Model for product
class Product(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='product')
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Product for {self.client.full_name} {self.price}")
    
#model for order
class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Order for {self.client.full_name} {self.amount} {self.order_date}") 