# Generated by Django 4.2.7 on 2024-04-18 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0055_alter_invoice_date_alter_invoice_invoice_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
