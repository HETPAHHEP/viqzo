# Generated by Django 4.2.2 on 2023-07-10 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_remove_usercampaign_unique_name_per_owner_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='shortlink',
            table='links_short_link',
        ),
    ]
