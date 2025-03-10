# Generated by Django 4.0.6 on 2024-11-29 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pojistenec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jmeno', models.CharField(max_length=100)),
                ('prijmeni', models.CharField(max_length=100)),
                ('adresa', models.CharField(max_length=255)),
                ('vek', models.IntegerField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Pojisteni',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ_pojisteni', models.CharField(choices=[('majetek', 'Pojištění majetku'), ('zivotni', 'Životní pojištění'), ('cestovni', 'Cestovní pojištění'), ('vozidla', 'Pojištění vozidel'), ('zdravotni', 'Zdravotní pojištění'), ('urazove', 'Úrazové pojištění'), ('odpovednost', 'Pojištění odpovědnosti'), ('domacnost', 'Pojištění domácnosti'), ('pravni_ochrana', 'Pojištění právní ochrany'), ('podnikani', 'Pojištění podnikatelských rizik')], max_length=50)),
                ('predmet_pojisteni', models.CharField(max_length=100)),
                ('datum_sjednani', models.DateField()),
                ('platnost_do', models.DateField()),
                ('castka', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pojistenec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pojisteni', to='NovyProjekt.pojistenec')),
            ],
        ),
        migrations.CreateModel(
            name='Uzivatel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=300, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PojistnaUdalost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum_udalosti', models.DateField()),
                ('popis', models.TextField()),
                ('status', models.CharField(choices=[('nahlaseno', 'Nahlášeno'), ('vyreseno', 'Vyřešeno'), ('ceka_na_schvaleni', 'Čeká na schválení')], max_length=20)),
                ('castka', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pojisteni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='udalosti', to='NovyProjekt.pojisteni')),
            ],
        ),
        migrations.AddField(
            model_name='pojistenec',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
