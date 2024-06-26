# Generated by Django 4.2.7 on 2024-03-09 10:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0019_remove_customer_customer_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_name', models.CharField(max_length=150)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_location', models.CharField(max_length=150)),
                ('order_amount', models.IntegerField()),
                ('order_status', models.CharField(choices=[('Delivered', 'Delivered'), ('In Progress', 'In Progress')], default='In Progress', max_length=15)),
            ],
        ),
    ]
