# Generated by Django 4.2 on 2024-03-09 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0020_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='phone',
            new_name='phone_number',
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
    ]
