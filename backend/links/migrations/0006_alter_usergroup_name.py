# Generated by Django 4.2.2 on 2024-02-19 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0005_alter_usergrouplink_alias_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Имя группы'),
        ),
    ]