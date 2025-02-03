from django import forms
from .models import Pojistenec, Pojisteni, PojistnaUdalost, Uzivatel


class UzivatelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:

        model = Uzivatel
        fields = ['first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hashování hesla
        if commit:
            user.save()
        return user

class PojistenecForm(forms.ModelForm):


    class Meta:
        model = Pojistenec
        fields = ['jmeno', 'prijmeni', 'adresa', 'vek', 'foto']

class PridaniForm(forms.ModelForm):


    class Meta:
        model = Pojisteni
        fields = ['typ_pojisteni', "predmet_pojisteni",
                  'datum_sjednani', 'platnost_do', 'castka']

class VyhledavaciForm(forms.Form):


    jmeno = forms.CharField(required=False, label='Jméno')
    prijmeni = forms.CharField(required=False, label='Příjmení')

class PojistnaUdalostForm(forms.ModelForm):


    class Meta:
        model = PojistnaUdalost
        fields = ['pojisteni', 'datum_udalosti',
                  'popis', 'status', 'castka']

class ZapomenuteHesloForm(forms.Form):


    email = forms.EmailField(label='E-mail', max_length=254)

class SetPasswordForm(forms.Form):


    new_password1 = forms.CharField(
        label='Nové heslo',  # Měníme název pro první pole
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Toto pole je povinné.'
        }
    )
    new_password2 = forms.CharField(
        label='Potvrdit nové heslo',  # Měníme název pro druhé pole
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Toto pole je povinné.'
        }
    )