from django.db import models
# from django.contrib.auth.models import User  # Optional, for user authentication
from django.utils import timezone
from datetime import datetime
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
    # MATERIAL_CHOICES = [
    #     ('mat1', 'MAT1'),
    #     ('mat2', 'MAT2'),
    #     ('mat3', 'MAT2'),
    #     ('mat4', 'MAT4'),
    # ]
    material_name = models.CharField(max_length=50, null=True)
    material_amt = models.IntegerField()
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.material_name



# class Customer(models.Model):
#     # customer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15, blank=True, null=True)

#     def __str__(self):
#         return self.name

# class Invoice(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)
    
#     STATUS_CHOICES = (
#         ('Paid', 'Paid'),
#         ('Pending', 'Pending'),
#     )
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

#     def __str__(self):
#         return f"Invoice for {self.customer.name}"
    
# class Order(models.Model):
#     # order_id = models.UUIDField(default=uuid.uuid4, editable = False, unique=True)
#     order_name = models.CharField(max_length=150)
#     # customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     order_date = models.DateTimeField(default=timezone.now)
#     order_location = models.CharField(max_length=150)
#     order_amount = models.IntegerField()
#     status_choices = (
#         ('Delivered', 'Delivered'),
#         ('In Progress', 'In Progress')
#     )
#     order_status = models.CharField(max_length=15, choices = status_choices, default='In Progress')


    

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=30, null=True)
    order_id = models.AutoField(primary_key=True)
    date = models.DateField()
    status_choices = (
        ('Finished', 'Finished'),
        ('In Progress', 'In Progress')
    )
    order_status = models.CharField(max_length=15, choices = status_choices, default='In Progress')
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is not yet saved in the database
            self.date = datetime.now()  # Set check_in to current datetime
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_name

class Invoice(models.Model):

    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=150, null=True)
    customer_name = models.CharField(max_length=100, blank=True)  # Allow blank since it will be auto-populated
    date = models.DateField()
    def save(self, *args, **kwargs):
        # Automatically fetch the customer name from the associated order
        self.customer_name = self.order.customer.name
        super().save(*args, **kwargs)

    status_choices = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid')
    )
    invoice_status = models.CharField(max_length=15, choices = status_choices, default='Unpaid')

    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is not yet saved in the database
            self.date = datetime.now()  # Set check_in to current datetime
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.order.customer.name}"
    

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=50, null=True,)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=30)
    rating = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.supplier_name
    

class Quotation(models.Model):
    id = models.AutoField(primary_key=True)
    quotation_name = models.CharField(max_length=20, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField()
    status_choices = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Under Review', 'Under Review')
    )
    quotation_status = models.CharField(max_length=15, choices = status_choices, default='Under Review')
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is not yet saved in the database
            self.date = datetime.now()  # Set check_in to current datetime
        super().save(*args, **kwargs)

    def __str__(self):
        return self.quotation_name
    

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_joining = models.DateField()
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is not yet saved in the database
            self.date_of_joining = datetime.now()  # Set check_in to current datetime
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Salary(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.CharField(max_length=7, blank=True, null=True)
    date = models.DateField()
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is not yet saved in the database
            self.date = datetime.now()  # Set check_in to current datetime
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name.name} - {self.date}"

    

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is not yet saved in the database
            self.check_in = datetime.now()  # Set check_in to current datetime
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.check_in.strftime('%Y-%m-%d %H:%M:%S')}"