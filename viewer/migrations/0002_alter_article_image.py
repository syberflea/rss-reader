# Generated by Django 5.2.3 on 2025-07-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.URLField(blank=True, null=True, verbose_name='Иконка'),
        ),
    ]
