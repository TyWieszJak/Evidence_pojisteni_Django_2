# forms.py
from django import forms
from .models import Pojistenec, Pojisteni,PojistnaUdalost

class PojistenecForm(forms.ModelForm):
    class Meta:
        model = Pojistenec
        fields = ['jmeno', 'prijmeni', 'adresa', 'vek', 'foto']

class PridaniForm(forms.ModelForm):
    class Meta:
        model = Pojisteni
        fields = ['typ_pojisteni',"predmet_pojisteni", 'datum_sjednani', 'platnost_do', 'castka']

class VyhledavaciForm(forms.Form):
    jmeno = forms.CharField(required=False, label='Jméno')
    prijmeni = forms.CharField(required=False, label='Příjmení')

class PojistnaUdalostForm(forms.ModelForm):
    class Meta:
        model = PojistnaUdalost
        fields = ['pojisteni', 'datum_udalosti', 'popis', 'status', 'castka']

class ZapomenuteHesloForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=254)