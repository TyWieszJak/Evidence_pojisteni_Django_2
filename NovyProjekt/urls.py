from django.urls import path
from . import views
from .views import seznam_pojistencu

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Domovská stránka

    # Cesty pro pojištěnce
    path('pojistenci/seznam_pojistencu/', views.seznam_pojistencu, name='seznam_pojistencu'),
    path('pridat-pojistence/', views.pridat_pojistence, name='pridat_pojistence'),
    path('pojistenci/uprav/pojistenec/<int:pk>/', views.upravit_pojistence, name='upravit_pojistence'),
    path('pojistenci/smazat/pojistenec/<int:pk>/', views.smazat_pojistence, name='smazat_pojistence'),
    path('pojistenci/detail/pojistenec/<int:pk>/', views.detail_pojistence, name='detail_pojistence'),

    # Cesty pro pojištění
    path('pojisteni/', views.seznam_pojisteni, name='seznam_pojisteni'),
    path('pojisteni/pridat/<int:pk>/', views.pridat_pojisteni, name='pridat_pojisteni'),
    path('pojisteni/uprav/<int:pk>/', views.upravit_pojisteni, name='upravit_pojisteni'),
    path('pojisteni/smazat/<int:pk>/', views.smazat_pojisteni, name='smazat_pojisteni'),

    # Přihlášení
    path('prihlaseni/', views.prihlaseni, name='prihlaseni'),
]
