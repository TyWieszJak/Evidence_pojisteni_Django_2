from django.core.management.base import BaseCommand
from NovyProjekt.models import Pojistenec
import csv


class Command(BaseCommand):
    help = ('Importuje data z CSV souboru do modelu Pojistenec'
            ' bez propojování s Uživatelem')

    def handle(self, *args, **kwargs):
        try:
            with open('NovyProjekt/management/commands/MOCK_DATA.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Vytvoření záznamu pro každého pojištěnce bez 'user' propojení
                    Pojistenec.objects.create(

                        jmeno=row['jmeno'],
                        prijmeni=row['prijmeni'],
                        adresa=row['adresa'],  # Zajišťujeme, že 'adresa' je součástí CSV
                        vek=row['vek'],
                    )

            self.stdout.write(self.style.SUCCESS('Data byla úspěšně importována.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Chyba při importu: {str(e)}'))
"""           
    def handle(self, user=None, *args, **kwargs):
        with open('NovyProjekt/management/commands/MOCK_DATA.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Pojistenec.objects.create(
                    user=user,  # Přiřazení uživatele podle emailu
                    jmeno=row['jmeno'],
                    prijmeni=row['prijmeni'],
                    adresa=row['adresa'],  # Zajišťujeme, že 'adresa' je součástí CSV
                    vek=row['vek'],
                )
            self.stdout.write(self.style.SUCCESS('Data byla úspěšně importována.'))
"""