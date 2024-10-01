from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404, redirect
from .models import Pojistenec, Pojisteni
from .forms import PojistenecForm, VyhledavaciForm, PridaniForm
from django.http import Http404

from django.shortcuts import render
from .models import Pojisteni
from .forms import VyhledavaciForm  # Zkontroluj, jestli máš tento formulář


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




def pridat_pojisteni(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk = pk)
    if request.method == "POST":
        form = PridaniForm(request.POST)
        if form.is_valid():
            pojisteni = form.save(commit=False)
            pojisteni.pojistenec = pojistenec
            pojisteni.save()
            return redirect('detail_pojistence', pk=pojistenec.pk)
    else:
        form = PridaniForm()
    return render(request, 'pojistenci/pridat_pojisteni.html', {'form': form , 'pojistenec': pojistenec})


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



def seznam_pojistencu(request):
    pojistenci = Pojistenec.objects.all()  # Získáme všechny pojištěnce
    paginator = Paginator(pojistenci, 9)  # Rozdělíme po 9 pojištěncích na stránku

    page_number = request.GET.get('page')  # Získáme aktuální stránku z parametru URL
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'pojistenci/seznam_pojistencu.html', context)

def smazat_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)  # Získáme konkrétního pojištěnce
    if request.method == 'POST':
        pojistenec.delete()  # Smažeme pojištěnce
        return redirect('seznam_pojistencu')  # Přesměrujeme na seznam pojištěnců
    return render(request, 'pojistenci/smazat_pojistence.html', {'pojistenec': pojistenec})

def detail_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)
    pojisteni = pojistenec.pojisteni.all()  # Získání všech pojištění pro daného pojištěnce

    return render(request, 'pojistenci/detail_pojistence.html', {
        'pojistenec': pojistenec,
        'pojisteni': pojisteni,  # Předání pojištění do šablony
    })

def upravit_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)
    if request.method == 'POST':
        form = PojistenecForm(request.POST, instance=pojistenec)
        if form.is_valid():
            form.save()
            return redirect('seznam_pojistencu')
    else:
        form = PojistenecForm(instance=pojistenec)

    return render(request, 'pojistenci/upravit_pojistence.html', {'form': form})

def pridat_pojistence(request):
    if request.method == 'POST':
        form = PojistenecForm(request.POST,request.FILES)
        if form.is_valid():
            print("Formulář je validní")
            form.save()
            return redirect('seznam_pojistencu')
        else:
            print("Formulář není validní", form.errors)
    else:
        form = PojistenecForm()

    return render(request, 'pojistenci/pridat_pojistence.html', {'form': form})

def index(request):
    return render(request, 'index.html')

from django.shortcuts import render

def prihlaseni(request):
    return render(request, 'pojistenci/login.html')