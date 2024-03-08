from django.db import models
# from django.contrib.auth.models import User  # Optional, for user authentication
from django.utils import timezone
# Create your models here.


class CustomerRequirements(models.Model):
    name = models.CharField(max_length=50, null=True)
    phone = models.IntegerField()
    email = models.EmailField(max_length=30)
    desc = models.CharField(max_length=150, null=True)
    surname = models.CharField(max_length=50, null=True) 
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    MATERIAL_CHOICES = [
        ('mat1', 'MAT1'),
        ('mat2', 'MAT2'),
        ('mat3', 'MAT2'),
        ('mat4', 'MAT4'),
    ]
    material_name = models.CharField(max_length=50, null=True, choices=MATERIAL_CHOICES)
    material_amt = models.IntegerField()

    def __str__(self):
        return self.material_name

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=50, null=True,)
    phone = models.IntegerField()
    email = models.EmailField(max_length=30)

    def __str__(self):
        return self.supplier_name
    



class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = (
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Invoice for {self.customer.name}"

    

