# Generated by Django 4.2.3 on 2023-08-04 11:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chef', '0002_alter_chef_experience_years'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chef',
            name='experience_years',
            field=models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
