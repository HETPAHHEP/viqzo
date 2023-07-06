# Generated by Django 4.2.2 on 2023-07-05 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0007_remove_aliasshortlink_unique_alias_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliasshortlink',
            name='original_link',
            field=models.URLField(max_length=2000, verbose_name='Оригинальная ссылка'),
        ),
        migrations.AddConstraint(
            model_name='aliasshortlink',
            constraint=models.UniqueConstraint(fields=('original_link', 'alias'), name='unique_alias_link'),
        ),
    ]
