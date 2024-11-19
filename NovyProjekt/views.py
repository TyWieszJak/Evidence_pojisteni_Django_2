from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, BasePermission
from .forms import PojistenecForm, VyhledavaciForm, PridaniForm, PojistnaUdalostForm
from django.contrib.auth.decorators import  user_passes_test
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib import messages
from .forms import ZapomenuteHesloForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User , Group
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import PojistnaUdalost
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import PojistnaUdalostSerializer

class IsOwnerOrAdmin(BasePermission):
    """
    Permission pro kontrolu, zda uživatel je vlastník nebo administrátor.
    """
    def has_permission(self, request, view):
        # Povolit přístup, pokud je uživatel přihlášen
        if not request.user.is_authenticated:
            return False
        # Povolit přístup, pokud je uživatel administrátor nebo vlastník (může být podle ID, role apod.)
        if request.user.is_staff or request.user == view.get_object().owner:
            return True
        return False


def admin(user):
    return user.groups.filter(name='Administrators').exists()
def pojisteny(user):
    return user.groups.filter(name='Insured').exists()

#@login_required
@user_passes_test(admin)
def pouze_administrator(request):
    # View přístupný pouze pro administrátory
    pass

#@login_required
@user_passes_test(pojisteny)
def pouze_uzivatel(request):
    # View přístupný pouze pro pojištěné
    pass

def index(request):
    return render(request, 'index.html')

class VytvorPojistnouUdalostAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Získáme všechny pojistné události přihlášeného uživatele
        pojistne_udalosti = PojistnaUdalost.objects.filter(pojistenec=request.user)
        serializer = PojistnaUdalostSerializer(pojistne_udalosti, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Validace a uložení nové pojistné události
        serializer = PojistnaUdalostSerializer(data=request.data)
        if serializer.is_valid():
            # Nastavíme pojistence na aktuálně přihlášeného uživatele
            serializer.save(pojistenec=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@login_required
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



class SeznamUdalostiAPI(APIView):
    permission_classes = [AllowAny]  # Zajistíme, že endpoint je přístupný pouze přihlášeným uživatelům

    def get(self, request):
        # Získáme pouze pojistné události přihlášeného uživatele
        events = PojistnaUdalost.objects.filter(pojistenec=request.user)
        serializer = PojistnaUdalostSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#@login_required
#@user_passes_test(pojisteny)
def seznam_ualosti(request):
    events = PojistnaUdalostForm.objects.filter(pojistenec=request.user)  # Pouze události přihlášeného uživatele
    return render(request, 'pojistne_udalosti/event_list.html', {'events': events})



class SeznamPojisteniAPI(ListAPIView):
    serializer_class = PojisteniSerializer
    permission_classes = [AllowAny]
    queryset = Pojisteni.objects.all()

    # Použití filtrů pro vyhledávání a třídění
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['typ_pojisteni', 'pojistenec__jmeno']  # Vyhledávání podle typu pojištění a jména pojištěnce
    ordering_fields = ['datum_sjednani']  # Třídění podle pole datum_sjednani
    ordering = ['-datum_sjednani']  # Výchozí třídění



#@login_required
#@user_passes_test(admin)
def seznam_pojisteni(request):
    # Inicializace formuláře pro vyhledávání
    vyhledavaci_form = VyhledavaciForm(request.GET or None)

    # Získání všech pojištění
    pojisteni = Pojisteni.objects.all().order_by('datum_sjednani')

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


class PridatPojisteniAPI(CreateAPIView):
    serializer_class = PojisteniSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Získání pojištěnce na základě pojistenec_id z URL
        pojistenec_id = kwargs.get('pojistenec_id')
        pojistenec = get_object_or_404(Pojistenec, pk=pojistenec_id)

        # Přiřazení pojištěnce a validace dat
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(pojistenec=pojistenec)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@login_required
#@user_passes_test(admin)
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



class UpravitPojisteniAPI(UpdateAPIView):
    serializer_class = PojisteniSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'  # Vyhledávání pojištění podle jeho PK v URL

    def get_object(self):
        # Získání pojištění podle ID z URL
        pojisteni = super().get_object()

        # Získání pojištěnce a kontrola, zda má uživatel přístup k pojištění
        if pojisteni.pojistenec != self.request.user:
            raise PermissionDenied("Nemáte oprávnění upravit toto pojištění.")
        return pojisteni

    def update(self, request, *args, **kwargs):
        # Získání pojištění, které se má upravit
        pojisteni = self.get_object()

        # Aktualizace pojištění
        serializer = self.get_serializer(pojisteni, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Uložení aktualizovaných dat
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@login_required
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


class SmazatPojisteniAPI(DestroyAPIView):
    serializer_class = PojisteniSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'  # Vyhledávání pojištění podle jeho PK v URL

    def get_object(self):
        # Získání pojištění podle ID z URL
        pojisteni = super().get_object()

        # Získání pojištěnce a kontrola, zda má uživatel přístup k pojištění
        if pojisteni.pojistenec != self.request.user:
            raise PermissionDenied("Nemáte oprávnění smazat toto pojištění.")
        return pojisteni

    def perform_destroy(self, instance):
        # Provádí smazání pojištění
        instance.delete()

    def delete(self, request, *args, **kwargs):
        # Provádí smazání a vrací odpověď
        self.get_object()  # Ověření, že uživatel má oprávnění
        return super().delete(request, *args, **kwargs)

#@login_required
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

class DetailPojisteniAPI(RetrieveAPIView):
    serializer_class = PojisteniSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'  # Vyhledávání pojištění podle jeho PK v URL

    def get_object(self):
        # Získání pojištění podle ID z URL
        pojisteni = super().get_object()

        # Ověření, zda má uživatel přístup k detailu pojištění (pokud je pojištěncem)
        if pojisteni.pojistenec != self.request.user:
            raise PermissionDenied("Nemáte oprávnění zobrazit detail tohoto pojištění.")
        return pojisteni

#@login_required
#@user_passes_test(pojisteny)
def detail_pojisteni(request, pk):
    pojisteni = get_object_or_404(Pojisteni, pk=pk)
    return render(request, 'pojistenci/detail_pojisteni.html', {'pojisteni': pojisteni})



class SeznamPojistencuAPI(ListAPIView):
    serializer_class = PojistenecSerializer
    permission_classes = [AllowAny]  # Pouze přihlášení uživatelé mohou zobrazit seznam pojištěnců
    filter_backends = [SearchFilter]
    search_fields = ['jmeno', 'prijmeni']  # Filtrace podle jména a příjmení
    page_size = 10  # Počet položek na stránku
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_queryset(self):
        # Načteme všechny pojištěnce
        queryset = Pojistenec.objects.all()

        # Pokud jsou ve GET parametrech filtry, použijeme je
        hledane_jmeno = self.request.query_params.get('jmeno', None)
        hledane_prijmeni = self.request.query_params.get('prijmeni', None)

        if hledane_jmeno:
            queryset = queryset.filter(jmeno__icontains=hledane_jmeno)

        if hledane_prijmeni:
            queryset = queryset.filter(prijmeni__icontains=hledane_prijmeni)

        # Seřazení podle jména
        return queryset.order_by('jmeno')

#@login_required
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

class SmazatPojistenceAPI(DestroyAPIView):
    queryset = Pojistenec.objects.all()
    serializer_class = PojistenecSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        # Získáme pojištěnce na základě pk z URL
        return get_object_or_404(Pojistenec, pk=self.kwargs['pk'])

    def perform_destroy(self, instance):
        # Vymažeme pojištěnce
        instance.delete()


#@login_required
#@user_passes_test(admin)
def smazat_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)  # Získáme konkrétního pojištěnce
    if request.method == 'POST':
        pojistenec.delete()  # Smažeme pojištěnce
        return redirect('seznam_pojistencu')  # Přesměrujeme na seznam pojištěnců
    return render(request, 'pojistenci/smazat_pojistence.html', {'pojistenec': pojistenec})



class DetailPojistenceAPI(RetrieveAPIView):
    queryset = Pojistenec.objects.all()
    serializer_class = PojistenecSerializer
    permission_classes = [AllowAny]  # Zajištění, že pouze přihlášení uživatelé mohou přistupovat k detailu

    def get_object(self):
        pojistenec = super().get_object()
        if self.request.user != pojistenec.user:  # Pokud uživatel není vlastníkem pojištěnce
            raise PermissionDenied("Nemáte oprávnění k těmto informacím.")
        return pojistenec

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Přidání pojištění do kontextu pro zobrazení v odpovědi
        context['pojisteni'] = Pojisteni.objects.filter(pojistenec=self.get_object())
        return context

#@login_required
#@user_passes_test(pojisteny)
def detail_pojistence(request, pk):
    pojistenec = get_object_or_404(Pojistenec, pk=pk)
    pojisteni = pojistenec.pojisteni.all()  # Získání všech pojištění pro daného pojištěnce

    return render(request, 'pojistenci/detail_pojistence.html', {
        'pojistenec': pojistenec,
        'pojisteni': pojisteni,  # Předání pojištění do šablony
    })

class UpravitPojistenceAPI(UpdateAPIView):
    queryset = Pojistenec.objects.all()
    serializer_class = PojistenecSerializer
    permission_classes = [AllowAny]  # Zajištění, že pouze přihlášení uživatelé mohou upravit pojištěnce

    def get_object(self):
        # Získání pojištěnce na základě pk z URL
        return get_object_or_404(Pojistenec, pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        # Volitelně můžete přidat logiku před uložením změn
        serializer.save()  # Uloží změny do databáze

#@login_required
#@user_passes_test(pojisteny)
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

class PridatPojistenceAPI(CreateAPIView):
    queryset = Pojistenec.objects.all()
    serializer_class = PojistenecSerializer
    permission_classes = [IsOwnerOrAdmin]  # Zajištění, že pouze přihlášení uživatelé mohou přidávat pojištěnce

    def perform_create(self, serializer):
        # Volitelně přidejte logiku pro nastavení dalších hodnot, jako je uživatel nebo nějaké defaultní hodnoty
        serializer.save()  # Uloží nového pojištěnce do databáze


#@login_required
#@user_passes_test(admin)
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
    #logger.debug("Toto je debug zpráva")
    return render(request, 'index.html')

def co_vidi(request):
    uzivatel = Uzivatel.objects.get(user=request.user)
    return render(request, 'your_template.html', {'user_profile': uzivatel})


class UzivatelProfilAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uzivatel = Uzivatel.objects.get(user=request.user)
        serializer = UzivatelSerializer(uzivatel)
        return Response(serializer.data)

class ZapomenuteHesloAPI(APIView):
    permission_classes = [AllowAny]  # Povolit přístup komukoli

    def post(self, request):
        # Vytvoření formuláře pro zapomenuté heslo
        form = ZapomenuteHesloForm(request.data)

        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)

                # Vytvoření resetovacího odkazu
                reset_link = request.build_absolute_uri(reverse('reset_heslo', args=[user.id]))

                # Odeslání e-mailu s odkazem na reset hesla
                send_mail(
                    'Obnovení hesla',
                    f'Klikněte na následující odkaz pro obnovení hesla: {reset_link}',
                    'noreply@vašeaplikace.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "Odkaz pro obnovení hesla byl odeslán na váš e-mail."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Uživatel s tímto e-mailem neexistuje."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

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



def odhlasit(request):
    logout(request)
    return redirect('index')

def prihlaseni(request):
    next_url = request.GET.get('next', 'index')  # Pokud není 'next', přesměruje na 'index'
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Byl jste úspěšně přihlášen!')
                return redirect(next_url)  # Přesměrování na předchozí nebo výchozí stránku
        else:
            messages.error(request, 'Nesprávné uživatelské jméno nebo heslo.')
    else:
        form = AuthenticationForm()
    return render(request, 'pojistenci/prihlaseni.html', {'form': form})

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
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')  # Získání vybrané role z formuláře
        if form.is_valid():
            user = form.save()
            if role == 'admin':
                group = Group.objects.get(name='Administrators')
            else:
                group = Group.objects.get(name='Insured')
            user.groups.add(group)  # Přiřazení uživatele do skupiny
            messages.success(request, 'Účet byl úspěšně vytvořen!')
            return redirect('prihlaseni')  # Přesměrování na stránku pro přihlášení
    else:
        form = UserCreationForm()
    return render(request, 'pojistenci/registrace.html', {'form': form})


#@login_required
#@user_passes_test(admin)
def seznam_pojistnych_udalosti(request):
    pojistne_udalosti = PojistnaUdalost.objects.all().order_by('status')
    paginator = Paginator(pojistne_udalosti, 10)  # 10 událostí na stránku
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pojistne_udalosti/seznam_pojistnych_udalosti.html', {'page_obj': page_obj})

#@login_required
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

#@login_required
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

#@login_required
#@user_passes_test(admin)
def smazat_pojistnou_udalost(request, id):
    pojistna_udalost = get_object_or_404(PojistnaUdalost, id=id)
    if request.method == 'POST':
        pojistna_udalost.delete()
        return redirect('seznam_pojistnych_udalosti')
    return render(request, 'pojistne_udalosti/smazat_pojistnou_udalost.html', {'pojistna_udalost': pojistna_udalost})
