# Generated by Django 4.2 on 2024-02-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabapp', '0007_remove_customerrequirements_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerrequirements',
            name='sex',
            field=models.BinaryField(null=True),
        ),
    ]
