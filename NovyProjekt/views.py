from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import  Pojisteni, PojistnaUdalost, Uzivatel # Pojistenec
from .forms import VyhledavaciForm, UzivatelForm # PojistenecForm
from .forms import PridaniForm, PojistnaUdalostForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


def admin(user):
    return user.groups.filter(name='Admin').exists()


def pojisteny(user):
    return user.groups.filter(name='pojistenec').exists()


@login_required
# @user_passes_test(pojisteny)
def vytvor_udalost(request):
    if request.method == 'POST':
        form = PojistnaUdalostForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.pojistenec = request.user
            event.save()
            return redirect('seznam_udalosti')
    else:
        form = PojistnaUdalostForm()
    return render(request, 'pojistne_udalosti/create_event.html',
                  {'form': form})


@login_required
# @user_passes_test(pojisteny)
def seznam_udalosti(request):
    events = PojistnaUdalostForm.objects.filter(pojistenec=request.user)  # Pouze události přihlášeného uživatele
    return render(request, 'pojistne_udalosti/event_list.html', {'events': events})


@login_required
# @user_passes_test(admin)
def seznam_pojisteni(request):
    vyhledavaci_form = VyhledavaciForm(request.GET or None)
    pojisteni = Pojisteni.objects.all()
    if vyhledavaci_form.is_valid():
        hledany_typ = vyhledavaci_form.cleaned_data.get('typ_pojisteni')
        if hledany_typ:
            pojisteni = pojisteni.filter(typ_pojisteni__icontains=hledany_typ)
        hledany_jmeno = vyhledavaci_form.cleaned_data.get('jmeno')
        if hledany_jmeno:
            pojisteni = pojisteni.filter(pojistenec__jmeno__icontains=hledany_jmeno)

    paginator = Paginator(pojisteni, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pojistenci/seznam_pojisteni.html', {
        'vyhledavaci_form': vyhledavaci_form,
        'pojisteni': page_obj,

    })


@login_required
# @user_passes_test(admin)
def pridat_pojisteni(request, pk):
    pojistenec = get_object_or_404(Uzivatel, pk=pk)
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
# @user_passes_test(admin)
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

    return render(request, 'pojistenci/upravit_pojisteni.html', {'form': form, 'pojistenec': pojistenec, 'pojisteni': pojisteni})


@login_required
# @user_passes_test(admin)
def smazat_pojisteni(request, pk):
    pojisteni = get_object_or_404(Pojisteni, pk=pk)
    pojistenec = pojisteni.pojistenec  # Získejte souvisejícího pojištěnce

    if request.method == 'POST':
        pojisteni.delete()
        return redirect('seznam_pojisteni')

    return render(request, 'pojistenci/smazat_pojisteni.html', {
        'pojisteni': pojisteni,
        'pojistenec': pojistenec
    })


@login_required
# @user_passes_test(pojisteny)
def detail_pojisteni(request, pk):
    pojisteni = get_object_or_404(Pojisteni, pk=pk)
    return render(request, 'pojistenci/detail_pojisteni.html', {'pojisteni': pojisteni})


def filter(request, queryset):
    jmeno = request.GET.get('jmeno', '')
    prijmeni = request.GET.get('prijmeni', '')
    if jmeno or prijmeni:
        queryset = queryset.filter(jmeno__icontains=jmeno, prijmeni__icontains=prijmeni)

    if request.GET.get('seradit') == 'true':  # Pokud je aktivováno třídění
        order_by = request.GET.get('order_by', 'jmeno')
        order_direction = request.GET.get('order_direction', 'asc')

        if order_by == 'jmeno':
            if order_direction == 'asc':
                queryset = queryset.order_by('jmeno')
            else:
                queryset = queryset.order_by('-jmeno')
    return queryset


@login_required
# @user_passes_test(admin)
def seznam_pojistencu(request):
    vyhledavaci_form = VyhledavaciForm()
    # pojistenci = Pojistenec.objects.all()
    # filterset = PojistenecFilter(request.GET, queryset=pojistenci)

    order_by = request.GET.get('order_by', 'first_name')
    order_direction = request.GET.get('order_direction', 'asc') or 'asc'

    if order_by not in ['first_name', 'last_name', 'vek', 'adresa']:
        order_by = 'first_name'

    if order_direction == 'desc':
        order_by = f'-{order_by}'

    pojistenci = Uzivatel.objects.all().order_by(order_by)
    # print(f"Jméno: {request.GET.get('jmeno')}, Příjmení: {request.GET.get('prijmeni')}")


    jmeno = request.GET.get('jmeno', '').strip() if request.GET.get('jmeno') else ''
    prijmeni = request.GET.get('prijmeni', '').strip() if request.GET.get('prijmeni') else ''

    if jmeno and prijmeni:
        pojistenci = pojistenci.filter(first_name__icontains=jmeno, last_name__icontains=prijmeni)
    elif jmeno:
        pojistenci = pojistenci.filter(first_name__icontains=jmeno)
    elif prijmeni:
        pojistenci = pojistenci.filter(last_name__icontains=prijmeni)

    paginator = Paginator(pojistenci, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'pojistenci/seznam_pojistencu.html', {
        'vyhledavaci_form': vyhledavaci_form,
        'page_obj': page_obj,
        # 'filterset': filterset,
        'order_by': order_by,
        'order_direction': order_direction,
    })


@login_required
# @user_passes_test(admin)
def smazat_pojistence(request, pk):
    pojistenec = get_object_or_404(Uzivatel, pk=pk)
    if request.method == 'POST':
        pojistenec.delete()
        return redirect('seznam_pojistencu')
    return render(request, 'pojistenci/smazat_pojistence.html', {'pojistenec': pojistenec})


@login_required
# @user_passes_test(pojisteny)
def detail_pojistence(request, pk):
    pojistenec = get_object_or_404(Uzivatel, pk=pk)
    pojisteni = pojistenec.pojisteni.all()

    return render(request, 'pojistenci/detail_pojistence.html', {
        'pojistenec': pojistenec,
        'pojisteni': pojisteni,
        'uzivatel': request.user
    })


@login_required
# @user_passes_test(pojisteny)
def upravit_pojistence(request, pk):
    pojistenec = get_object_or_404(Uzivatel, pk=pk)
    if request.method == 'POST':
        form = UzivatelForm(request.POST, request.FILES, instance=pojistenec)
        if form.is_valid():
            form.save()
            return redirect('seznam_pojistencu')
    else:
        form = UzivatelForm(instance=pojistenec)

    return render(request, 'pojistenci/upravit_pojistence.html', {'form': form})


@login_required
# @user_passes_test(admin)
def pridat_pojistence(request):
    if request.method == 'POST':
        form = UzivatelForm(request.POST, request.FILES)
        if form.is_valid():
            print("Formulář je validní")
            pojistenec = form.save(commit=False)
            pojistenec.save()
            form.save()
            return redirect('seznam_pojistencu')
        else:
            form = UzivatelForm()
    else:
        form = UzivatelForm()

    return render(request, 'pojistenci/pridat_pojistence.html', {'form': form})


def index(request):
    logger.debug("Toto je debug zpráva")
    return render(request, 'index.html')


class Zapomenute_Heslo(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'pojistenci/zapomenute_heslo.html', {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = Uzivatel.objects.filter(email=email)
            if users.exists():
                for user in users:
                    token = default_token_generator.make_token(user)
                    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
                    # reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[uidb64, token]))
                    """
                    send_mail(
                        'Obnovení hesla',
                        f'Klikněte na tento odkaz pro obnovení hesla: {reset_link}',
                        'noreply@vašeaplikace.com',
                        [email],
                        fail_silently=False,
                    )
                    """
                    return redirect('password_reset_confirm', uidb64=uidb64, token=token)
                messages.success(request, 'Odkaz pro obnovení hesla byl odeslán na váš e-mail.')
            else:
                messages.error(request, 'Uživatel s tímto e-mailem neexistuje.')
            return redirect('zapomenute_heslo')
        return render(request, 'pojistenci/password_reset_confirm.html', {'form': form})


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Uzivatel.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                form = SetPasswordForm(user)
                return render(request, 'pojistenci/password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
            else:
                messages.error(request, "Odkaz na resetování hesla není platný.")
                return redirect('zapomenute_heslo')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Odkaz na resetování hesla není platný.")
            return redirect('zapomenute_heslo')

    def post(self, request, uidb64, token):
        DEFAULT_PASSWORD = "heslojeveslo"
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Uzivatel.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    if user.email == "demo@example.com":
                        user.set_password(DEFAULT_PASSWORD)
                        user.save()
                        messages.success(request, "Heslo pro testovací účet bylo vráceno na původní hodnotu.")
                    messages.success(request, 'Vaše heslo bylo úspěšně obnoveno.')
                    return redirect('zapomenute_heslo')
                else:
                    # print(form.errors)
                    messages.error(request, "Formulář obsahuje chyby.")
                    return render(request, 'pojistenci/password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
            else:
                messages.error(request, "Odkaz na resetování hesla není platný.")
                return redirect('zapomenute_heslo')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Odkaz na resetování hesla není platný.")
            return redirect('zapomenute_heslo')


# @login_required
def odhlasit(request):
    logout(request)
    return redirect('index')


# @login_required
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
            user.save()
            messages.success(request, 'Účet byl úspěšně vytvořen!')
            return redirect('prihlaseni')
    else:
        form = UzivatelForm()
    return render(request, 'pojistenci/registrace.html', {'form': form})


@login_required
# @user_passes_test(admin)
def seznam_pojistnych_udalosti(request):
    pojistne_udalosti = PojistnaUdalost.objects.all().order_by('status')
    paginator = Paginator(pojistne_udalosti, 10)  # 10 událostí na stránku
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pojistne_udalosti/seznam_pojistnych_udalosti.html', {'page_obj': page_obj})


@login_required
# @user_passes_test(pojisteny)
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
# @user_passes_test(admin)
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
# @user_passes_test(admin)
def smazat_pojistnou_udalost(request, id):
    pojistna_udalost = get_object_or_404(PojistnaUdalost, id=id)
    if request.method == 'POST':
        pojistna_udalost.delete()
        return redirect('seznam_pojistnych_udalosti')
    return render(request, 'pojistne_udalosti/smazat_pojistnou_udalost.html', {'pojistna_udalost': pojistna_udalost})
