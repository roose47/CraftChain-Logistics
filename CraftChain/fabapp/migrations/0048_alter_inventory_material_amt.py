# Generated by Django 4.2 on 2024-03-19 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0047_alter_inventory_material_amt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='material_amt',
            field=models.IntegerField(),
        ),
    ]
