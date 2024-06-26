# Generated by Django 4.2 on 2024-03-09 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0021_remove_invoice_customer_delete_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_status', models.CharField(choices=[('Delivered', 'Delivered'), ('In Progress', 'In Progress')], default='In Progress', max_length=15)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fabapp.customer')),
            ],
        ),
    ]
