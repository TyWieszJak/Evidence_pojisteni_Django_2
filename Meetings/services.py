from django.shortcuts import get_object_or_404
from .models import Schuzka
from NovyProjekt.models import Uzivatel


class SchuzkaService:
    @staticmethod
    def create_schuzka(data):
        user = get_object_or_404(Uzivatel, id=data.pojistenec_id)
        return Schuzka.objects.create(
            pojistenec=user,
            datum_cas=data.datum_cas,
            poznamka=data.poznamka
        )

    @staticmethod
    def list_schuzky():
        return Schuzka.objects.all()

    @staticmethod
    def get_schuzka(schuzka_id):
        return get_object_or_404(Schuzka, id=schuzka_id)

    @staticmethod
    def delete_schuzka(schuzka_id):
        schuzka = get_object_or_404(Schuzka, id=schuzka_id)
        schuzka.delete()
        return {"message": "Schůzka byla smazána."}
