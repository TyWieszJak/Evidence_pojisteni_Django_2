from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404, redirect
from .models import Pojistenec, Pojisteni, PojistnaUdalost , Uzivatel
from .forms import PojistenecForm, VyhledavaciForm, PridaniForm, PojistnaUdalostForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import ZapomenuteHesloForm, UzivatelForm
from django.core.mail import send_mail
from django.views import View
from django.urls import reverse
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User , Group
import logging

logger = logging.getLogger(__name__)


def admin(user):
    return user.groups.filter(name='Administrators').exists()
def pojisteny(user):
    return user.groups.filter(name='Insured').exists()

@login_required
@user_passes_test(admin)
def pouze_administrator(request):
    # View přístupný pouze pro administrátory
    pass

@login_required
@user_passes_test(pojisteny)
def pouze_uzivatel(request):
    # View přístupný pouze pro pojištěné
    pass

@login_required
#@user_passes_test(pojisteny)
def vytvor_ualost(request):
    if request.method == 'POST':
        form = PojistnaUdalostForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.pojistenec = request.user  # Událost se váže na přihlášeného uživatele
            event.save()
            return redirect('seznam_udalosti')  # Redirect na seznam pojistných událostí
    else:
        form = PojistnaUdalostForm()
    return render(request, 'pojistne_udalosti/create_event.html', {'form': form})

@login_required
#@user_passes_test(pojisteny)
def seznam_ualosti(request):
    events = PojistnaUdalostForm.objects.filter(pojistenec=request.user)  # Pouze události přihlášeného uživatele
    return render(request, 'pojistne_udalosti/event_list.html', {'events': events})

@login_required
#@user_passes_test(admin)
def seznam_pojisteni(request):
    # Inicializace formuláře pro vyhledávání
    vyhledavaci_form = VyhledavaciForm(request.GET or None)

    # Získání všech pojištění
    pojisteni = Pojisteni.objects.all()

    # Zpracování formuláře pro vyhledávání
    if vyhledavaci_form.is_valid():
        # Získání hodnot z formuláře
        hledany_typ = vyhledavaci_form.cleaned_data.get('typ_pojisteni')

        # Filtrování podle hledaného typu pojištění, pokud je zadaný
        if hledany_typ:
            pojisteni = pojisteni.filter(typ_pojisteni__icontains=hledany_typ)

        # Příklad: pokud chceš filtrovat podle jména pojištěnce
        hledany_jmeno = vyhledavaci_form.cleaned_data.get('jmeno')
        if hledany_jmeno:
            pojisteni = pojisteni.filter(pojistenec__jmeno__icontains=hledany_jmeno)

    paginator = Paginator(pojisteni, 10)  # 10 pojištění na stránku
    page_number = request.GET.get('page')  # Získání čísla stránky z URL
    page_obj = paginator.get_page(page_number)  # Získání stránky

    # Vrátí stránku se seznamem pojištění a vyhledávacím formulářem
    return render(request, 'pojistenci/seznam_pojisteni.html', {
        'vyhledavaci_form': vyhledavaci_form,
        'pojisteni': page_obj,

    })



@login_required
#@user_passes_test(admin)
def pridat_pojisteni(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk = pk)
    if request.method == "POST":
        form = PridaniForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            pojisteni = form.save(commit=False)
            pojisteni.pojistenec = pojistenec
            pojisteni.save()
            return redirect('detail_pojistence', pk=pojistenec.pk)
    else:
        form = PridaniForm()
    return render(request, 'pojistenci/pridat_pojisteni.html', {'form': form , 'pojistenec': pojistenec})

@login_required
#@user_passes_test(admin)
def upravit_pojisteni(request, pk):
    pojisteni = get_object_or_404(Pojisteni, pk=pk)
    pojistenec = pojisteni.pojistenec  # Získání pojištěnce z pojištění

    if request.method == 'POST':
        form = PridaniForm(request.POST, instance=pojisteni)
        if form.is_valid():
            form.save()
            return redirect('detail_pojistence', pk=pojistenec.pk)
    else:
        form = PridaniForm(instance=pojisteni)

    return render(request, 'pojistenci/upravit_pojisteni.html', {'form': form, 'pojistenec': pojistenec,'pojisteni': pojisteni,})


@login_required
#@user_passes_test(admin)
def smazat_pojisteni(request, pk):
    # Získání pojištění k odstranění
    pojisteni = get_object_or_404(Pojisteni, pk=pk)
    pojistenec = pojisteni.pojistenec  # Získejte souvisejícího pojištěnce

    if request.method == 'POST':
        pojisteni.delete()
        return redirect('seznam_pojisteni')

    return render(request, 'pojistenci/smazat_pojisteni.html', {
        'pojisteni': pojisteni,
        'pojistenec': pojistenec  # Předejte objekt pojistenec do kontextu
    })


@login_required
#@user_passes_test(pojisteny)
def detail_pojisteni(request, pk):
    pojisteni = get_object_or_404(Pojisteni, pk=pk)
    return render(request, 'pojistenci/detail_pojisteni.html', {'pojisteni': pojisteni})

@login_required
#@user_passes_test(admin)
def seznam_pojistencu(request):
    vyhledavaci_form = VyhledavaciForm()
    pojistenci = Pojistenec.objects.all()

    if request.GET.get('jmeno') or request.GET.get('prijmeni'):
        jmeno = request.GET.get('jmeno')
        prijmeni = request.GET.get('prijmeni')
        pojistenci = pojistenci.filter(jmeno__icontains=jmeno, prijmeni__icontains=prijmeni)

    # Paginace
    paginator = Paginator(pojistenci, 10)  # 10 pojištěnců na stránku
    page_number = request.GET.get('page')  # Získejte číslo stránky z dotazu
    try:
        page_obj = paginator.get_page(page_number)  # Získejte příslušnou stránku
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)  # Pokud není číslo stránky, vraťte první stránku
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Pokud je stránka prázdná, vraťte poslední stránku

    return render(request, 'pojistenci/seznam_pojistencu.html', {
        'vyhledavaci_form': vyhledavaci_form,
        'page_obj': page_obj,  # Předáváme paginovaný objekt
    })

@login_required
#@user_passes_test(admin)
def smazat_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)  # Získáme konkrétního pojištěnce
    if request.method == 'POST':
        pojistenec.delete()  # Smažeme pojištěnce
        return redirect('seznam_pojistencu')  # Přesměrujeme na seznam pojištěnců
    return render(request, 'pojistenci/smazat_pojistence.html', {'pojistenec': pojistenec})

@login_required
#@user_passes_test(pojisteny)
def detail_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)
    pojisteni = pojistenec.pojisteni.all()  # Získání všech pojištění pro daného pojištěnce

    return render(request, 'pojistenci/detail_pojistence.html', {
        'pojistenec': pojistenec,
        'pojisteni': pojisteni,  # Předání pojištění do šablony
        'uzivatel': request.user
    })

@login_required
#@user_passes_test(pojisteny)
def upravit_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)
    if request.method == 'POST':
        form = PojistenecForm(request.POST,request.FILES, instance=pojistenec)
        if form.is_valid():
            form.save()
            return redirect('seznam_pojistencu')
    else:
        form = PojistenecForm(instance=pojistenec)

    return render(request, 'pojistenci/upravit_pojistence.html', {'form': form})

@login_required
#@user_passes_test(admin)
def pridat_pojistence(request):
    if request.method == 'POST':
        form = PojistenecForm(request.POST,request.FILES)
        if form.is_valid():
            print("Formulář je validní")
            pojistenec = form.save(commit=False)
           # pojistenec.user = request.user  # Zde přiřazujeme přihlášeného uživatele
            pojistenec.save()
            form.save()
            return redirect('seznam_pojistencu')
        else:
            form = PojistenecForm()
    else:
        form = PojistenecForm()

    return render(request, 'pojistenci/pridat_pojistence.html', {'form': form})

def index(request):
    logger.debug("Toto je debug zpráva")
    return render(request, 'index.html')

def co_vidi(request):
    uzivatel = Uzivatel.objects.get(user=request.user)
    return render(request, 'your_template.html', {'user_profile': uzivatel})


#@login_required
class Zapomenute_Heslo(View):
    def get(self, request):
        form = ZapomenuteHesloForm()
        return render(request, 'pojistenci/zapomenute_heslo.html', {'form': form})

    def post(self, request):
        form = ZapomenuteHesloForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Odeslat e-mail s odkazem na reset hesla
                reset_link = request.build_absolute_uri(reverse('reset_heslo', args=[user.id]))
                send_mail(
                    'Obnovení hesla',
                    f'Klikněte na následující odkaz pro obnovení hesla: {reset_link}',
                    'noreply@vašeaplikace.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Odkaz pro obnovení hesla byl odeslán na váš e-mail.')
            except User.DoesNotExist:
                messages.error(request, 'Uživatel s tímto e-mailem neexistuje.')
            return redirect('prihlaseni')  # Přesměrování na přihlašovací stránku
        return render(request, 'zapomenute_heslo.html', {'form': form})

#@login_required
def odhlasit(request):
    logout(request)
    return redirect('index')

#@login_required
def prihlaseni(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Byl jste úspěšně přihlášen!')
                return redirect('index')  # Přesměrování po úspěšném přihlášení
        else:
            messages.error(request, 'Nesprávné uživatelské jméno nebo heslo.')
    else:
        form = AuthenticationForm()
    return render(request, 'pojistenci/prihlaseni.html', {'form': form})

def registrace(request):
    if request.method == 'POST':
        form = UzivatelForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Účet byl úspěšně vytvořen!')
            return redirect('prihlaseni')  # Přesměrování na stránku pro přihlášení
    else:
        form = UzivatelForm()
    return render(request, 'pojistenci/registrace.html', {'form': form})


@login_required
#@user_passes_test(admin)
def seznam_pojistnych_udalosti(request):
    pojistne_udalosti = PojistnaUdalost.objects.all().order_by('status')
    paginator = Paginator(pojistne_udalosti, 10)  # 10 událostí na stránku
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pojistne_udalosti/seznam_pojistnych_udalosti.html', {'page_obj': page_obj})

@login_required
#@user_passes_test(pojisteny)
# Přidání nové pojistné události
def pridat_pojistnou_udalost(request):
    if request.method == 'POST':
        form = PojistnaUdalostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seznam_pojistnych_udalosti')
    else:
        form = PojistnaUdalostForm()
    return render(request, 'pojistne_udalosti/pridat_pojistnou_udalost.html', {'form': form})

@login_required
#@user_passes_test(admin)
def upravit_pojistnou_udalost(request, id):
    pojistna_udalost = get_object_or_404(PojistnaUdalost, id=id)
    if request.method == 'POST':
        form = PojistnaUdalostForm(request.POST, instance=pojistna_udalost)
        if form.is_valid():
            form.save()
            return redirect('seznam_pojistnych_udalosti')
    else:
        form = PojistnaUdalostForm(instance=pojistna_udalost)
    return render(request, 'pojistne_udalosti/upravit_pojistnou_udalost.html', {'form': form})

@login_required
#@user_passes_test(admin)
def smazat_pojistnou_udalost(request, id):
    pojistna_udalost = get_object_or_404(PojistnaUdalost, id=id)
    if request.method == 'POST':
        pojistna_udalost.delete()
        return redirect('seznam_pojistnych_udalosti')
    return render(request, 'pojistne_udalosti/smazat_pojistnou_udalost.html', {'pojistna_udalost': pojistna_udalost})