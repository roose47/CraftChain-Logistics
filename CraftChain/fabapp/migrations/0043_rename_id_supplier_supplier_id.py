# Generated by Django 4.2 on 2024-03-16 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0042_alter_inventory_id_alter_supplier_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='id',
            new_name='supplier_id',
        ),
    ]
