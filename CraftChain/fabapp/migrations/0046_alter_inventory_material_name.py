# Generated by Django 4.2 on 2024-03-19 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0045_rename_order_status_invoice_invoice_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='material_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
