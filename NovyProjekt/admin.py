from django.contrib import admin
from .models import Uzivatel, Pojistenec, Pojisteni, PojistnaUdalost


# Registrace vlastního uživatelského modelu
@admin.register(Uzivatel)
class UzivatelAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin')
    search_fields = ('email',)
    list_filter = ('is_admin',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Oprávnění', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_admin'),
        }),
    )


# Registrace modelu Pojistenec
@admin.register(Pojistenec)
class PojistenecAdmin(admin.ModelAdmin):
    list_display = ('jmeno', 'prijmeni', 'adresa', 'vek', 'user')
    search_fields = ('jmeno', 'prijmeni', 'adresa')
    list_filter = ('vek',)
    ordering = ('prijmeni',)
    raw_id_fields = ('user',)


# Registrace modelu Pojisteni
@admin.register(Pojisteni)
class PojisteniAdmin(admin.ModelAdmin):
    list_display = ('pojistenec', 'typ_pojisteni', 'datum_sjednani', 'platnost_do', 'castka')
    search_fields = ('typ_pojisteni', 'pojistenec__jmeno', 'pojistenec__prijmeni')
    list_filter = ('typ_pojisteni', 'datum_sjednani')
    ordering = ('-datum_sjednani',)


# Registrace modelu PojistnaUdalost
@admin.register(PojistnaUdalost)
class PojistnaUdalostAdmin(admin.ModelAdmin):
    list_display = ('pojisteni', 'datum_udalosti', 'status', 'castka')
    search_fields = ('pojisteni__typ_pojisteni', 'status')
    list_filter = ('status', 'datum_udalosti')
    ordering = ('-datum_udalosti',)
