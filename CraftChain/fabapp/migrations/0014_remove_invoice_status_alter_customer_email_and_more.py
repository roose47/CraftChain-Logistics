# Generated by Django 4.2 on 2024-03-07 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0013_remove_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='status',
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
