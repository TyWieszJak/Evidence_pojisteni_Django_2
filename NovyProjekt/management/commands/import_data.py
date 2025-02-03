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
                    Pojistenec.objects.create(

                        jmeno=row['jmeno'],
                        prijmeni=row['prijmeni'],
                        adresa=row['adresa'],
                        vek=row['vek'],
                    )

            self.stdout.write(self.style.SUCCESS('Data byla úspěšně importována.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Chyba při importu: {str(e)}'))
