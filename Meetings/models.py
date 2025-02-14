from django.db import models
from django.utils import timezone
from NovyProjekt.models import Uzivatel


class Schuzka(models.Model):
    pojistenec = models.ForeignKey(
        Uzivatel,
        on_delete=models.CASCADE,
        related_name='schuzky'
    )
    datum_cas = models.DateTimeField(default=timezone.now)
    poznamka = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Schůzka u {self.pojistenec} dne {self.datum_cas}"
