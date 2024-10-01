from django.contrib import admin
from .models import Pojistenec  # Importuj svůj model

@admin.register(Pojistenec)
class PojistenecAdmin(admin.ModelAdmin):
    list_display = ('jmeno', 'prijmeni')  # Zobrazí tato pole v seznamu
