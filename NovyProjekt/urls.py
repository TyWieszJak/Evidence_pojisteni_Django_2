from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from . import views
from .views import seznam_pojistencu

from django.urls import path
from . import views
from .viewsAPI import smazat_pojistence

urlpatterns = [
    path('', views.index, name='index'),  # Domovská stránka

    # Cesty pro pojištěnce
    #path('pojistenci/seznam_pojistencu/', views.seznam_pojistencu, name='seznam_pojistencu'),
    #path('pridat-pojistence/', views.pridat_pojistence, name='pridat_pojistence'),
    #path('pojistenci/uprav/pojistenec/<int:pk>/', views.upravit_pojistence, name='upravit_pojistence'),
    #path('pojistenci/smazat/pojistenec/<int:pk>/', views.smazat_pojistence, name='smazat_pojistence'),
    #path('pojistenci/detail/pojistenec/<int:pk>/', views.detail_pojistence, name='detail_pojistence'),

    # Cesty pro pojištění
    path('pojisteni/', views.seznam_pojisteni, name='seznam_pojisteni'),
    path('pojisteni/<int:pk>/', views.detail_pojisteni, name='detail_pojisteni'),
    path('pojisteni/pridat/<int:pk>/', views.pridat_pojisteni, name='pridat_pojisteni'),
    path('pojisteni/uprav/<int:pk>/', views.upravit_pojisteni, name='upravit_pojisteni'),
    path('pojisteni/smazat/<int:pk>/', views.smazat_pojisteni, name='smazat_pojisteni'),

    # Cesty pro pojištění na účely událostí
    path('pojistne_udalosti/', views.seznam_pojistnych_udalosti, name='seznam_pojistnych_udalosti'),
    path('pojistne_udalosti/pridat/', views.pridat_pojistnou_udalost, name='pridat_pojistnou_udalost'),
    path('pojistne_udalosti/upravit/<int:id>/', views.upravit_pojistnou_udalost, name='upravit_pojistnou_udalost'),
    path('pojistne_udalosti/smazat/<int:id>/', views.smazat_pojistnou_udalost, name='smazat_pojistnou_udalost'),

    # Cesty pro přihlášení, registraci, a odhlášení
    path('pojistenci/prihlaseni/', views.prihlaseni, name='prihlaseni'),
    path('pojistenci/registrace/', views.registrace, name='registrace'),
    path('odhlasit/', views.odhlasit, name='odhlasit'),

    path('pojistenci/zapomenute_heslo/', views.Zapomenute_Heslo.as_view(), name='zapomenute_heslo'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # cesty pro API
    path('pojistenci/', views.seznam_pojistencu, name='api_seznam_pojistencu'),
    path('pojistenci/pridat/', views.pridat_pojistence, name='api_pridat_pojistence'),
    path('pojistenci/<int:pk>/', views.detail_pojistence, name='api_detail_pojistence'),
    path('pojistenci/<int:pk>/upravit/', views.upravit_pojistence, name='api_upravit_pojistence'),
    path('pojistenci/<int:pk>/smazat/', views.smazat_pojistence, name='api_smazat_pojistence'),
]
