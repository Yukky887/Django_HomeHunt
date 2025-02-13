# Generated by Django 4.2.17 on 2025-02-10 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_home_original_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='original_address',
            field=models.URLField(blank=True, help_text='Уникальный URL с оригинального сайта', null=True, unique=True),
        ),
    ]
