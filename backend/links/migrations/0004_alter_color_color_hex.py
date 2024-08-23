# Generated by Django 4.2.2 on 2024-08-23 09:04

import django.core.validators
from django.db import migrations, models
import links.validators


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_color_alter_usergroup_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='color_hex',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=4), django.core.validators.MaxLengthValidator(limit_value=7), links.validators.HexColorValidator], verbose_name='HEX Цвета'),
        ),
    ]
