# Generated by Django 4.2.2 on 2024-02-15 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0004_alter_usergrouplink_alias_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergrouplink',
            name='alias_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_links', to='links.aliasshortlink', verbose_name='Пользовательская ссылка группы'),
        ),
        migrations.AlterField(
            model_name='usergrouplink',
            name='short_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_links', to='links.shortlink', verbose_name='Короткая ссылка группы'),
        ),
    ]