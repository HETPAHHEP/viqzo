# Generated by Django 4.2.2 on 2023-07-05 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0006_alter_aliasshortlink_table'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='aliasshortlink',
            name='unique_alias_link',
        ),
    ]
