# Generated by Django 5.0.3 on 2024-03-11 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0038_invoice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotation',
            old_name='quotaion_name',
            new_name='quotation_name',
        ),
    ]
