from django.urls import path

from . import views
from .views import *
from rest_framework_simplejwt import views as jwt_views
from .views import SmazatPojisteniAPI,DetailPojisteniAPI



urlpatterns = [
    # Cesty pro pojištěnce
    path('', views.index, name='index'),  # Domovská stránka
    path('pojistenci/seznam_pojistencu/', views.seznam_pojistencu, name='seznam_pojistencu'),
    path('pridat-pojistence/',views.pridat_pojistence, name='pridat_pojistence'),
    path('pojistenci/uprav/pojistenec/<int:pk>/', views.upravit_pojistence, name='upravit_pojistence'),
    path('pojistenci/smazat/pojistenec/<int:pk>/', views.smazat_pojistence, name='smazat_pojistence'),
    path('pojistenci/detail/pojistenec/<int:pk>/', views.detail_pojistence, name='detail_pojistence'),

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

    path('prihlaseni/', views.prihlaseni, name='prihlaseni'),
    path('registrace/', views.registrace, name='registrace'),
    path('odhlasit/', views.odhlasit, name='odhlasit'),
    path('zapomenute_heslo/', Zapomenute_Heslo.as_view(), name='Zapomenute_heslo'),
    path('admin-only/', views.pouze_administrator, name='admin_only'),
    path('insured-only/', views.pouze_uzivatel, name='insured_only'),

    # Tokeny
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),


    # Cesty pro API
    path('api/vytvor_udalost/', VytvorPojistnouUdalostAPI.as_view(), name='vytvor_udalost_api'),
    path('api/udalosti/', SeznamUdalostiAPI.as_view(), name='seznam_udalosti_api'),
    path('api/pojisteni/', SeznamPojisteniAPI.as_view(), name='seznam_pojisteni_api'),
    path('api/pridat-pojisteni/<int:pojistenec_id>/', PridatPojisteniAPI.as_view(), name='pridat_pojisteni_api'),
    path('api/upravit-pojisteni/<int:pk>/', UpravitPojisteniAPI.as_view(), name='upravit_pojisteni_api'),
    path('api/smazat-pojisteni/<int:pk>/', SmazatPojisteniAPI.as_view(), name='smazat_pojisteni_api'),
    path('api/detail-pojisteni/<int:pk>/', DetailPojisteniAPI.as_view(), name='detail_pojisteni_api'),
    path('api/seznam-pojistencu/', SeznamPojistencuAPI.as_view(), name='seznam_pojistencu_api'),
    path('api/smazat-pojistence/<int:pk>/', SmazatPojistenceAPI.as_view(), name='smazat_pojistence_api'),
    path('api/detail-pojistence/<int:pk>/', DetailPojistenceAPI.as_view(), name='detail_pojistence_api'),
    path('api/upravit-pojistence/<int:pk>/', UpravitPojistenceAPI.as_view(), name='upravit_pojistence_api'),
    path('api/pridat-pojistence/', PridatPojistenceAPI.as_view(), name='pridat_pojistence_api'),
    path('api/profil/', UzivatelProfilAPI.as_view(), name='profil_api'),
    path('api/zapomenute-heslo/', ZapomenuteHesloAPI.as_view(), name='zapomenute_heslo_api'),

]
