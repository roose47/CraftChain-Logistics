# Generated by Django 5.0.3 on 2024-03-12 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0039_rename_quotaion_name_quotation_quotation_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotation',
            old_name='supplier_name',
            new_name='supplier',
        ),
    ]
