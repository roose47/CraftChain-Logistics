# Generated by Django 4.2 on 2024-03-09 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0024_order_order_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_name',
        ),
    ]
