# forms.py
from django import forms
from .models import Pojistenec, Pojisteni

class PojistenecForm(forms.ModelForm):
    class Meta:
        model = Pojistenec
        fields = ['jmeno', 'prijmeni', 'adresa', 'vek', 'foto']

class PridaniForm(forms.ModelForm):
    class Meta:
        model = Pojisteni
        fields = ['typ_pojisteni', 'datum_sjednani', 'platnost_do', 'castka']

class VyhledavaciForm(forms.Form):
    jmeno = forms.CharField(required=False, label='Jméno')
    prijmeni = forms.CharField(required=False, label='Příjmení')
