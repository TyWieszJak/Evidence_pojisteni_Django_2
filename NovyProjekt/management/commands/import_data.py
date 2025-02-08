from django.core.management.base import BaseCommand
from NovyProjekt.models import Uzivatel
import csv


class Command(BaseCommand):
    help = ('Importuje data z CSV souboru do modelu Uzivatel')

    def handle(self, *args, **kwargs):
        try:
            with open('NovyProjekt/management/commands/MOCK_DATA.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    email = f"{row['first_name'].lower()}.{row['last_name'].lower()}@example.com"

                    uzivatel, created = Uzivatel.objects.get_or_create(
                        email=email,
                        defaults={
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                            'adresa': row['adresa'],
                            'vek': row['vek'],
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f"Uživatel {row['first_name']} {row['last_name']} vytvořen s emailem {email}."))
                    else:
                        self.stdout.write(self.style.WARNING(f"Uživatel s emailem {email} již existuje."))
            self.stdout.write(self.style.SUCCESS('Data byla úspěšně importována.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Chyba při importu: {str(e)}'))
