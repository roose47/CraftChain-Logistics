# Generated by Django 5.0.2 on 2024-03-18 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0044_rename_supplier_id_supplier_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='order_status',
            new_name='invoice_status',
        ),
    ]