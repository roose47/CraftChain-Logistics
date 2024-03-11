# Generated by Django 5.0.3 on 2024-03-11 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0037_delete_invoice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='fabapp.order')),
                ('invoice_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.CharField(max_length=150, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', max_length=15)),
            ],
        ),
    ]
