# Generated by Django 5.1.2 on 2025-01-07 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NovyProjekt', '0004_uzivatel_first_name_uzivatel_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uzivatel',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
