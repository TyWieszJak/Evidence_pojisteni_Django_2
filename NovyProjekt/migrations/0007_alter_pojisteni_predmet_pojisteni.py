# Generated by Django 5.0 on 2024-10-02 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NovyProjekt', '0006_alter_pojisteni_predmet_pojisteni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pojisteni',
            name='predmet_pojisteni',
            field=models.CharField(default=None, max_length=100),
        ),
    ]