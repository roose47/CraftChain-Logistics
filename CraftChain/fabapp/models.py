from django.db import models

# Create your models here.


class CustomerRequirements(models.Model):
    name = models.CharField(max_length=50, null=True)
    phone = models.IntegerField()
    email = models.EmailField(max_length=30)
    desc = models.CharField(max_length=150, null=True)

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

class RawMaterials(models.Model):
    RAW_MATERIAL_CHOICES = [
        ('rm1', 'RM1'),
        ('rm2', 'RM2'),
        ('rm3', 'RM2'),
        ('rm4', 'RM4'),
    ]
    raw_material_name = models.CharField(max_length=50, null=True, choices=RAW_MATERIAL_CHOICES)
    raw_material_amt = models.IntegerField()

    def __str__(self):
        return self.raw_material_name
    