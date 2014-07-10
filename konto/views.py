#-*- encoding: utf-8 -*-
import random
import datetime
import decimal

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.models import User

from models import RegistrationProfile, RejestracjaKlienta, Zamowienia, KontaBankowe

# from django.shortcuts import get_object_or_404
from django.contrib import auth
from oferta.models import Koszyk, Dodatki_Id
from django.core.context_processors import csrf
from forms import LoginForm, RejestracjaUsera, PlatnoscKlienta, RealizacjaZamowienia, Kontakt
# from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from reportlab.pdfgen import canvas

CART_ID_SESSION_KEY = 'cart_id'


def czas_now():
    return datetime.datetime.now()


def _cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRQSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id


def activate(request, activation_key, template_name='konto/activate.html'):

    activation_key = activation_key.lower()
    account = RegistrationProfile.objects.activate_user(activation_key)
    from django.contrib.auth.models import User
    # email po kliknieciu w link aktywacyjny
    from django.core.mail import send_mail
    subject = 'Twoje konto na SafeServer.pl zostało aktywowane.'
    message = render_to_string('konto/activation_done_email.txt')
    user = User.objects.get(id=account.user_id)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    return render_to_response(template_name,
                              {'account': account, 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS},
                              context_instance=RequestContext(request))


def register(request, success_url='/rejestracja/zakonczona/', form_class=RejestracjaUsera, profile_callback=None,
             template_name='konto/rejesracja.html'):

    if request.method == 'POST':
        formers = RejestracjaUsera(data=request.POST, files=request.FILES)
        if formers.is_valid():
            new_user = formers.save(profile_callback=profile_callback)
            return HttpResponseRedirect(success_url)
    else:
        # formers = RejestracjaUsera()
        formers = form_class
    return render_to_response(template_name, {'formers': formers}, context_instance=RequestContext(request))


def login(request):

    if request.POST:

        form = LoginForm(request.POST)
        logowanie = request.POST.get('login_panel', '')
        haslowanie = request.POST.get('haslo_panel', '')

        if form.is_valid():
            user_sprzed = auth.authenticate(username=logowanie, password=haslowanie)
            try:
                r = RegistrationProfile.objects.get(user_id=user_sprzed)
                aktywny = r.ACTIVATED
                klucz = r.activation_key
            except RegistrationProfile.DoesNotExist:
                aktywny = ''
                klucz = ''

            # nie kasowac przyda sie przy debugowaniu
            # if klucz == aktywny:
            #     print aktywny
            #     print klucz
            # else:
            #     print aktywny
            #     print klucz

            # sprawdza przy logowaniu czy user jest 'ALREADY_ACTIVATED'
            if user_sprzed is not None and klucz == aktywny:
                auth.login(request, user_sprzed)
                return HttpResponseRedirect('/konto_klienta/')
            else:
                return HttpResponseRedirect('/login/')
    else:
        form = LoginForm()
    c = {'form': form}
    c.update(csrf(request))

    return render_to_response('konto/login.html', c, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def konto(request):
    form_rejestr = RejestracjaKlienta.objects.filter(user_id=request.user.id)

    for f in form_rejestr:
        imie = f.imie
        nazwisko = f.nazwisko
        adres = f.adres
        kod = f.kod_pocztowy
        miasto = f.miasto
        kraj = f.kraj
        wojewodztwo = f.wojewodztwo
        telefon = f.telefon
        tel_dodatkowy = f.telefon_dodatkowy
        nazwafirmy = f.nazwa_firmy
        nip = f.nip
        regon = f.regon

        try:
            queryset = Zamowienia.objects.filter(user_id=request.user.id).order_by('-date_added').all()
            c = {'query': queryset, 'imie': imie, 'nazwisko': nazwisko, 'adres': adres, 'kod': kod, 'miasto': miasto,
                 'kraj': kraj, 'wojewodztwo': wojewodztwo, 'telefon': telefon, 'tel_dodatkowy': tel_dodatkowy,
                 'nazwafirmy': nazwafirmy, 'nip': nip, 'regon': regon}
            return render_to_response('konto/konto_klienta.html', c, context_instance=RequestContext(request))

        except Zamowienia.DoesNotExist:

            c = {'imie': imie, 'nazwisko': nazwisko, 'adres': adres, 'kod': kod, 'miasto': miasto, 'kraj': kraj,
                 'wojewodztwo': wojewodztwo, 'telefon': telefon, 'tel_dodatkowy': tel_dodatkowy,
                 'nazwafirmy': nazwafirmy, 'nip': nip, 'regon': regon}
            return render_to_response('konto/konto_klienta.html', c, context_instance=RequestContext(request))


@login_required
def daneklienta_koszy(request):

    form_rejestr = RejestracjaKlienta.objects.filter(user_id=request.user.id)

    numer = RejestracjaKlienta.objects.get(user_id=request.user.id)
    numeracja = numer.user_id
    pikater = Koszyk.objects.get(cart_id=_cart_id(request))
    pikater.user_id = numeracja
    pikater.save()

    for f in form_rejestr:
        imie = f.imie
        nazwisko = f.nazwisko
        adres = f.adres
        kod = f.kod_pocztowy
        miasto = f.miasto
        kraj = f.kraj
        wojewodztwo = f.wojewodztwo
        telefon = f.telefon
        tel_dodatkowy = f.telefon_dodatkowy
        nazwafirmy = f.nazwa_firmy
        nip = f.nip
        regon = f.regon

        cenoweryte = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
        cennka = cenoweryte.amount
        cennka_brutto = cenoweryte.total_amount

        vat_podatk = cennka_brutto - cennka

        if request.POST:

            return HttpResponseRedirect('/platnosc/')

        c = {'imie': imie, 'nazwisko': nazwisko, 'adres': adres, 'kod': kod, 'miasto': miasto, 'kraj': kraj,
             'wojewodztwo': wojewodztwo, 'telefon': telefon, 'tel_dodatkowy': tel_dodatkowy, 'nazwafirmy': nazwafirmy,
             'nip': nip, 'regon': regon, 'cennka': cennka, 'cennka_brutto': cennka_brutto, 'vat_podatk': vat_podatk}
        c.update(csrf(request))

        return render_to_response('konto/dane_klienta_koszyk.html', c, context_instance=RequestContext(request))


@login_required
def platnosc(request):

    cenoweryte = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
    cennka = cenoweryte.amount
    cennka_brutto = cenoweryte.total_amount

    vat_podatk = cennka_brutto - cennka

    if request.POST:

        place = PlatnoscKlienta(request.POST)

        if place.is_valid():

            wybor_place = request.POST.get('like')

            platnosci = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
            platnosci.platnosc = wybor_place
            platnosci.save()

            if wybor_place == '1':
                return HttpResponseRedirect('/podsumowanie_przelewy24/')
            elif wybor_place == '2':
                return HttpResponseRedirect('/podsumowanie_paypal/')
            else:
                return HttpResponseRedirect('/podsumowanie_przelew_zwykly/')

    else:
        place = PlatnoscKlienta()

    c = {'place':place,'cennka':cennka,'cennka_brutto':cennka_brutto,'vat_podatk':vat_podatk}
    c.update(csrf(request))

    return render_to_response("konto/platnosc.html",c, context_instance=RequestContext(request))


@login_required
def podsumowanie_przelewy24(request):
    return render_to_response("konto/podsumowanie_przelew24.html", context_instance=RequestContext(request))


@login_required
def podsumowanie_paypal(request):
    body_html = 'konto/informacja_o_zamowieniu_do_klienta.html'
    body_html2 = 'konto/informacja_o_zamowieniu_do_safeserver.html'
    body_html3 = 'konto/status_zamowienia_paypal.html'

    filtr_koszyk = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
    rejestrator_klik = RejestracjaKlienta.objects.get(user_id=request.user.id)

    login_userr = rejestrator_klik.user
    imie_me = rejestrator_klik.imie
    nazwisko_me = rejestrator_klik.nazwisko
    fakturaa = rejestrator_klik.faktura_vat
    telefonn = rejestrator_klik.telefon
    telefonn_dodat = rejestrator_klik.telefon_dodatkowy
    adress = rejestrator_klik.adres
    kod_pocztek = rejestrator_klik.kod_pocztowy
    miastoo = rejestrator_klik.miasto
    krajj = rejestrator_klik.kraj
    wojewodd = rejestrator_klik.wojewodztwo
    nazwa_firmyy = rejestrator_klik.nazwa_firmy
    nip_fir = rejestrator_klik.nip
    regon_fir = rejestrator_klik.regon

    userrter = User.objects.get(username__exact=login_userr)
    email_me = userrter.email

    # szukanie ostatniego id Zamowienia
    z = Zamowienia.objects.all().order_by('-id')
    # id zwiekszam o 1
    try:
        idt = z[0].id + 1
    except:
        idt = 1

    data_koszyk = filtr_koszyk.date_added

    data_ter = czas_now()
    waznosc_ter = datetime.datetime(data_ter.year+1, data_ter.month, data_ter.day)
    waznosc = waznosc_ter.strftime('%d-%m-%Y')
    oferta = filtr_koszyk.oferta
    dadatek = filtr_koszyk.dodatki
    platnosc = filtr_koszyk.platnosc
    suma_netto = filtr_koszyk.amount
    suma_brutto = filtr_koszyk.total_amount
    cena_netto_oferta = filtr_koszyk.cena
    cena_brutto_oferta = decimal.Decimal(float(filtr_koszyk.cena) * 1.23)

    podatek_vat = suma_brutto - suma_netto

    if oferta == 1:
        nazwa_ofert = 'SafeServer Starter'
    elif oferta == 2:
        nazwa_ofert = 'SafeServer Standard'
    elif oferta == 3:
        nazwa_ofert = 'SafeServer Buisness'
    else:
        nazwa_ofert = 'SafeServer Professional'

    if platnosc == 1:
        nazwa_platnosc = 'Przelewy24'
    elif platnosc == 2:
        nazwa_platnosc = 'PayPal'
    else:
        nazwa_platnosc = 'Przelew zwykły'

    if dadatek == 0:
        dodatek = 'Brak dodatków'
    else:
        dodatek = '+Dodatki'

    if fakturaa is True:
        faktura_nazwa = 'Wersja papierowa i elektroniczna'
    else:
        faktura_nazwa = 'Wersja elektroniczna'

    pay_nazwa = '%s %s' % (nazwa_ofert, dodatek)

    if request.POST:

        formaterker = RealizacjaZamowienia(request.POST)

        if formaterker.is_valid():
            login = request.POST.get('login')
            nazwa_serwera = request.POST.get('nazwa_serwera')
            imie = request.POST.get('imie')
            nazwisko = request.POST.get('nazwisko')
            rodzaj_platnosci = request.POST.get('rodzaj_platnosci')
            suma_netto_ter = request.POST.get('suma_netto')
            suma_brutto_ter = request.POST.get('suma_brutto')
            numer_zamowienia = request.POST.get('numer_zamowienia')
            data_zamowienia = request.POST.get('data_zamowienia')

            # pobranie listy obiektow Dodatki_Id
            d = Dodatki_Id.objects.filter(cart_id=_cart_id(request), czas_dodatki=data_koszyk)
            list_dodatki = []
            for i in d:
                # wyciaganie nazw z Dodatki poprzez relacje
                a = i.dodatki_id.nazwa
                list_dodatki.append(a)

            html_content = render_to_string(body_html, {
                'pay_nazwa': nazwa_ofert, 'list_dodatki': list_dodatki, 'platnosc': platnosc, 'regon_fir': regon_fir,
                'nip_fir': nip_fir, 'nazwa_firmyy': nazwa_firmyy, 'email_me': email_me, 'telefonn': telefonn,
                'telefonn_dodat': telefonn_dodat, 'wojewodd': wojewodd, 'krajj': krajj, 'adress': adress,
                'kod_pocztek': kod_pocztek, 'miastoo': miastoo, 'login': login, 'nazwa_serwera': nazwa_serwera,
                'imie': imie, 'nazwisko': nazwisko, 'rodzaj_platnosci': rodzaj_platnosci,
                'suma_netto_ter': suma_netto_ter, 'suma_brutto_ter': suma_brutto_ter,
                'numer_zamowienia': numer_zamowienia, 'data_zamowienia': data_zamowienia})

            text_content = strip_tags(html_content)

            html_content2 = render_to_string(body_html2, {
                'pay_nazwa': nazwa_ofert, 'list_dodatki': list_dodatki, 'platnosc': platnosc, 'regon_fir': regon_fir,
                'nip_fir': nip_fir, 'nazwa_firmyy': nazwa_firmyy, 'email_me': email_me, 'telefonn': telefonn,
                'telefonn_dodat': telefonn_dodat, 'wojewodd': wojewodd, 'krajj': krajj, 'adress': adress,
                'kod_pocztek': kod_pocztek, 'miastoo': miastoo, 'login': login, 'nazwa_serwera': nazwa_serwera,
                'imie': imie, 'nazwisko': nazwisko, 'rodzaj_platnosci': rodzaj_platnosci,
                'suma_netto_ter': suma_netto_ter, 'suma_brutto_ter': suma_brutto_ter,
                'numer_zamowienia': numer_zamowienia, 'data_zamowienia': data_zamowienia})

            text_content2 = strip_tags(html_content2)

            html_content3 = render_to_string(body_html3, {'numer_zamowienia': numer_zamowienia,
                                                          'data_zamowienia': data_zamowienia})
            text_content3 = strip_tags(html_content3)

            subject = 'Informacja o zamowieniu nr. %s z dnia %s | SafeServer.pl' % (numer_zamowienia, data_zamowienia)

            mail = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email_me])
            mail.attach_alternative(html_content, "text/html")
            # mail.send()
            # print 'mail do klienta - info o zamowieniu'

            subject3 = 'Status zamowienia %s z dnia %s - Oczekiwanie na platnosc PayPal | SafeServer.pl' % \
                       (numer_zamowienia, data_zamowienia)

            mail3 = EmailMultiAlternatives(subject3, text_content3, settings.EMAIL_HOST_USER, [email_me])
            mail3.attach_alternative(html_content3, "text/html")
            # mail3.send()
            # print 'mail do klienta - oczekiwanie na platnosc'

            subject2 = 'Zamowienie nr. %s z dnia %s | SafeServer.pl' % (numer_zamowienia, data_zamowienia)

            mail2 = EmailMultiAlternatives(subject2, text_content2, settings.EMAIL_HOST_USER, ['biuro@safeserver.pl'])
            mail2.attach_alternative(html_content2, "text/html")
            # mail2.send()
            # print 'mail do biura'

            zamowienie_klik, create = Zamowienia.objects.get_or_create(id=idt, cart_id=_cart_id(request),
                                                                       date_added=data_koszyk, user_id=request.user.id)
            zamowienie_klik.login = login
            zamowienie_klik.nazwa_serwera = nazwa_serwera
            zamowienie_klik.imie = imie
            zamowienie_klik.nazwisko = nazwisko
            zamowienie_klik.rodzaj_platnosci = rodzaj_platnosci
            zamowienie_klik.suma_netto = suma_netto_ter
            zamowienie_klik.suma_brutto = suma_brutto_ter
            zamowienie_klik.numer_zamowienia = numer_zamowienia
            zamowienie_klik.data_zamowienia = data_zamowienia
            zamowienie_klik.cart_id = _cart_id(request)
            zamowienie_klik.date_added = data_koszyk
            zamowienie_klik.data_waznosci = waznosc
            zamowienie_klik.suma_netto_oferta = cena_netto_oferta
            zamowienie_klik.suma_brutto_oferta = cena_brutto_oferta
            wybrane_dodatki = Dodatki_Id.objects.filter(cart_id=_cart_id(request), czas_dodatki=data_koszyk)

            for a in wybrane_dodatki:
                zamowienie_klik.dodatki.add(a.id)
            zamowienie_klik.save()
            return HttpResponseRedirect('/konto_klienta/zamowienie_paypal/')

    else:
        formaterker = RealizacjaZamowienia()

    c = {'formaterker': formaterker, 'idt': idt, 'data_ter': data_ter, 'nazwa_ofert': nazwa_ofert, 'dodatek': dodatek,
         'suma_netto': suma_netto, 'suma_brutto': suma_brutto, 'podatek_vat': podatek_vat,
         'nazwa_platnosc': nazwa_platnosc, 'pay_nazwa': pay_nazwa, 'login_userr': login_userr, 'imie_me': imie_me,
         'nazwisko_me': nazwisko_me, 'email_me': email_me, 'faktura_nazwa': faktura_nazwa, 'telefonn': telefonn}
    c.update(csrf(request))
    return render_to_response("konto/podsumowanie_paypal.html", c, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def platnoscpaypalzaakceptowana(request):
    return render_to_response("konto/platnosc_paypal_zaakceptowana.html", context_instance=RequestContext(request))


@login_required
@csrf_exempt
def platnoscpaypalodrzucona(request):
    return render_to_response("konto/platnosc_paypal_odrzucona.html", context_instance=RequestContext(request))


@login_required
def podsumowanie_przelew(request):

    body_html = 'konto/informacja_o_zamowieniu_do_klienta.html'
    body_html2 = 'konto/informacja_o_zamowieniu_do_safeserver.html'
    body_html3 = 'konto/status_zamowienia.html'

    filtr_koszyk = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
    rejestrator_klik = RejestracjaKlienta.objects.get(user_id=request.user.id)

    login_userr = rejestrator_klik.user
    imie_me = rejestrator_klik.imie
    nazwisko_me = rejestrator_klik.nazwisko
    fakturaa = rejestrator_klik.faktura_vat
    telefonn = rejestrator_klik.telefon
    telefonn_dodat = rejestrator_klik.telefon_dodatkowy
    adress = rejestrator_klik.adres
    kod_pocztek = rejestrator_klik.kod_pocztowy
    miastoo = rejestrator_klik.miasto
    krajj = rejestrator_klik.kraj
    wojewodd = rejestrator_klik.wojewodztwo
    nazwa_firmyy = rejestrator_klik.nazwa_firmy
    nip_fir = rejestrator_klik.nip
    regon_fir = rejestrator_klik.regon

    # szukanie ostatniego id Zamowienia
    z = Zamowienia.objects.all().order_by('-id')
    # id zwiekszam o 1
    try:
        idt = z[0].id + 1
    except:
        idt = 1

    data_koszyk = filtr_koszyk.date_added
    userrter = User.objects.get(username__exact=login_userr)
    email_me = userrter.email

    data_ter = czas_now()
    waznosc_ter = datetime.datetime(data_ter.year+1, data_ter.month, data_ter.day)
    waznosc = waznosc_ter.strftime('%d-%m-%Y')
    oferta = filtr_koszyk.oferta
    dadatek = filtr_koszyk.dodatki
    platnosc = filtr_koszyk.platnosc
    suma_netto = filtr_koszyk.amount
    suma_brutto = filtr_koszyk.total_amount
    cena_netto_oferta = filtr_koszyk.cena
    cena_brutto_oferta = decimal.Decimal(float(filtr_koszyk.cena) * 1.23)

    podatek_vat = suma_brutto - suma_netto

    if oferta == 1:
        nazwa_ofert = 'SafeServer Starter'
    elif oferta == 2:
        nazwa_ofert = 'SafeServer Standard'
    elif oferta == 3:
        nazwa_ofert = 'SafeServer Buisness'
    else:
        nazwa_ofert = 'SafeServer Professional'

    if platnosc == 1:
        nazwa_platnosc = 'Przelewy24'
    elif platnosc == 2:
        nazwa_platnosc = 'PayPal'
    else:
        nazwa_platnosc = 'Przelew zwykły'

    if dadatek == 0:
        dodatek = 'Brak dodatków'
    else:
        dodatek = '+ Dodatki'

    if fakturaa is True:
        faktura_nazwa = 'Wersja papierowa i elektroniczna'
    else:
        faktura_nazwa = 'Wersja elektroniczna'

    pay_nazwa = '%s %s' % (nazwa_ofert, dodatek)

    if request.POST:

        formaterker = RealizacjaZamowienia(request.POST)

        if formaterker.is_valid():
            login = request.POST.get('login')
            nazwa_serwera = request.POST.get('nazwa_serwera')
            imie = request.POST.get('imie')
            nazwisko = request.POST.get('nazwisko')
            rodzaj_platnosci = request.POST.get('rodzaj_platnosci')
            suma_netto_ter = request.POST.get('suma_netto')
            suma_brutto_ter = request.POST.get('suma_brutto')
            numer_zamowienia = request.POST.get('numer_zamowienia')
            data_zamowienia = request.POST.get('data_zamowienia')

            # pobranie listy obiektow Dodatki_Id
            d = Dodatki_Id.objects.filter(cart_id=_cart_id(request), czas_dodatki=data_koszyk)
            list_dodatki = []
            for i in d:
                # wyciaganie nazw z Dodatki poprzez relacje
                a = i.dodatki_id.nazwa
                list_dodatki.append(a)

            html_content = render_to_string(body_html, {
                'pay_nazwa': nazwa_ofert, 'list_dodatki': list_dodatki, 'platnosc': platnosc, 'regon_fir': regon_fir,
                'nip_fir': nip_fir, 'nazwa_firmyy': nazwa_firmyy, 'email_me': email_me, 'telefonn': telefonn,
                'telefonn_dodat': telefonn_dodat, 'wojewodd': wojewodd, 'krajj': krajj, 'adress': adress,
                'kod_pocztek': kod_pocztek, 'miastoo': miastoo, 'login': login, 'nazwa_serwera': nazwa_serwera,
                'imie': imie, 'nazwisko': nazwisko, 'rodzaj_platnosci': rodzaj_platnosci,
                'suma_netto_ter': suma_netto_ter, 'suma_brutto_ter': suma_brutto_ter,
                'numer_zamowienia': numer_zamowienia, 'data_zamowienia': data_zamowienia})

            text_content = strip_tags(html_content)

            html_content2 = render_to_string(body_html2, {
                'pay_nazwa': nazwa_ofert, 'list_dodatki': list_dodatki, 'platnosc': platnosc, 'regon_fir': regon_fir,
                'nip_fir': nip_fir, 'nazwa_firmyy': nazwa_firmyy, 'email_me': email_me, 'telefonn': telefonn,
                'telefonn_dodat': telefonn_dodat, 'wojewodd': wojewodd, 'krajj': krajj, 'adress': adress,
                'kod_pocztek': kod_pocztek, 'miastoo': miastoo, 'login': login, 'nazwa_serwera': nazwa_serwera,
                'imie': imie, 'nazwisko': nazwisko, 'rodzaj_platnosci': rodzaj_platnosci,
                'suma_netto_ter': suma_netto_ter, 'suma_brutto_ter': suma_brutto_ter,
                'numer_zamowienia': numer_zamowienia, 'data_zamowienia': data_zamowienia})

            text_content2 = strip_tags(html_content2)

            html_content3 = render_to_string(body_html3, {'numer_zamowienia': numer_zamowienia,
                                                          'data_zamowienia': data_zamowienia})
            text_content3 = strip_tags(html_content3)

            subject = 'Informacja o zamowieniu nr. %s z dnia %s | SafeServer.pl' % (numer_zamowienia, data_zamowienia)

            mail = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email_me])
            mail.attach_alternative(html_content, "text/html")
            # mail.send()

            subject3 = 'Status zamowienia %s z dnia %s - Oczekiwanie na przelew | SafeServer.pl' % (numer_zamowienia,
                                                                                                    data_zamowienia)

            mail3 = EmailMultiAlternatives(subject3, text_content3, settings.EMAIL_HOST_USER, [email_me])
            mail3.attach_alternative(html_content3, "text/html")
            # mail3.send()

            subject2 = 'Zamowienie nr. %s z dnia %s | SafeServer.pl' % (numer_zamowienia, data_zamowienia)

            mail2 = EmailMultiAlternatives(subject2, text_content2, settings.EMAIL_HOST_USER, ['biuro@safeserver.pl'])
            mail2.attach_alternative(html_content2, "text/html")
            # mail2.send()

            zamowienie_klik, create = Zamowienia.objects.get_or_create(id=idt, cart_id=_cart_id(request),
                                                                       date_added=data_koszyk, user_id=request.user.id)
            zamowienie_klik.login = login
            zamowienie_klik.nazwa_serwera = nazwa_serwera
            zamowienie_klik.imie = imie
            zamowienie_klik.nazwisko = nazwisko
            zamowienie_klik.rodzaj_platnosci = rodzaj_platnosci
            zamowienie_klik.suma_netto = suma_netto_ter
            zamowienie_klik.suma_brutto = suma_brutto_ter
            zamowienie_klik.numer_zamowienia = numer_zamowienia
            zamowienie_klik.data_zamowienia = data_zamowienia
            zamowienie_klik.cart_id = _cart_id(request)
            zamowienie_klik.date_added = data_koszyk
            zamowienie_klik.data_waznosci = waznosc
            zamowienie_klik.suma_netto_oferta = cena_netto_oferta
            zamowienie_klik.suma_brutto_oferta = cena_brutto_oferta
            wybrane_dodatki = Dodatki_Id.objects.filter(cart_id=_cart_id(request), czas_dodatki=data_koszyk)

            for a in wybrane_dodatki:
                zamowienie_klik.dodatki.add(a.id)
            zamowienie_klik.save()
            return HttpResponseRedirect('/konto_klienta/zamowienie_przelew/')

    else:
        formaterker = RealizacjaZamowienia()

    c = {'formaterker': formaterker, 'idt': idt, 'data_ter': data_ter, 'nazwa_ofert': nazwa_ofert, 'dodatek': dodatek,
         'suma_netto': suma_netto, 'suma_brutto': suma_brutto, 'podatek_vat': podatek_vat,
         'nazwa_platnosc': nazwa_platnosc, 'pay_nazwa': pay_nazwa, 'login_userr': login_userr, 'imie_me': imie_me,
         'nazwisko_me': nazwisko_me, 'email_me': email_me, 'faktura_nazwa': faktura_nazwa, 'telefonn': telefonn}
    c.update(csrf(request))
    return render_to_response("konto/podsumowanie_przelew.html", c, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def zamowienieprzelew(request):
    # trzeba pobrac date z koszyka
    filtr_koszyk = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
    # i dodatkowo przefiltrowac zamowienia po dacie z koszyka, bo inaczej wywala blad - multiple object
    # przyczyna - te same cart_id
    zamowienie = Zamowienia.objects.get(cart_id=_cart_id(request), user_id=request.user.id,
                                        date_added=filtr_koszyk.date_added)
    numer_dane = zamowienie.numer_zamowienia
    data_zami = zamowienie.data_zamowienia
    c = {'numer_dane': numer_dane, 'data_zami': data_zami}
    c.update(csrf(request))
    return render_to_response("konto/zamowienie_przelew.html", c, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def zamowienieprzelew_zestawienie(request, slug):

    zamowienie = Zamowienia.objects.get(id=slug, user_id=request.user.id)
    numer_dane = zamowienie.numer_zamowienia
    data_zami = zamowienie.data_zamowienia
    c = {'numer_dane': numer_dane, 'data_zami': data_zami}
    c.update(csrf(request))
    return render_to_response("konto/zamowienie_przelew.html", c, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def zamowieniepaypal(request):

    filtr_koszyk = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
    rejestrator_klik = RejestracjaKlienta.objects.get(user_id=request.user.id)
    zamowienie = Zamowienia.objects.get(cart_id=_cart_id(request), user_id=request.user.id,
                                        date_added=filtr_koszyk.date_added)

    login_userr = rejestrator_klik.user
    imie_me = rejestrator_klik.imie
    nazwisko_me = rejestrator_klik.nazwisko
    fakturaa = rejestrator_klik.faktura_vat
    telefonn = rejestrator_klik.telefon

    userrter = User.objects.get(username__exact=login_userr)
    email_me = userrter.email

    idt = zamowienie.id
    data_ter = czas_now()
    oferta = filtr_koszyk.oferta
    dadatek = filtr_koszyk.dodatki
    platnosc = filtr_koszyk.platnosc
    suma_netto = filtr_koszyk.amount
    suma_brutto = filtr_koszyk.total_amount

    podatek_vat = suma_brutto - suma_netto

    if oferta == 1:
        nazwa_ofert = 'SafeServer Starter'
    elif oferta == 2:
        nazwa_ofert = 'SafeServer Standard'
    elif oferta == 3:
        nazwa_ofert = 'SafeServer Buisness'
    else:
        nazwa_ofert = 'SafeServer Professional'

    if platnosc == 1:
        nazwa_platnosc = 'Przelewy24'
    elif platnosc == 2:
        nazwa_platnosc = 'PayPal'
    else:
        nazwa_platnosc = 'Przelew zwykły'

    if dadatek == 0:
        dodatek = 'Brak dodatków'
    else:
        dodatek = '+ Dodatki'

    if fakturaa is True:
        faktura_nazwa = 'Wersja papierowa i elektroniczna'
    else:
        faktura_nazwa = 'Wersja elektroniczna'

    pay_nazwa = '%s %s' % (nazwa_ofert, dodatek)

    c = {'idt': idt, 'data_ter': data_ter, 'nazwa_ofert': nazwa_ofert, 'dodatek': dodatek, 'suma_netto': suma_netto,
         'suma_brutto': suma_brutto, 'podatek_vat': podatek_vat, 'nazwa_platnosc': nazwa_platnosc,
         'pay_nazwa': pay_nazwa, 'login_userr': login_userr, 'imie_me': imie_me, 'nazwisko_me': nazwisko_me,
         'email_me': email_me, 'faktura_nazwa': faktura_nazwa, 'telefonn': telefonn}
    return render_to_response("konto/zamowienie_paypal.html", c, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def zamowieniepaypal_zestawienie(request, slug):

    rejestrator_klik = RejestracjaKlienta.objects.get(user_id=request.user.id)
    zamowienie = Zamowienia.objects.get(id=slug, user_id=request.user.id)

    login_userr = rejestrator_klik.user
    imie_me = rejestrator_klik.imie
    nazwisko_me = rejestrator_klik.nazwisko
    fakturaa = rejestrator_klik.faktura_vat
    telefonn = rejestrator_klik.telefon

    userrter = User.objects.get(username__exact=login_userr)
    email_me = userrter.email

    idt = zamowienie.id
    data_ter = czas_now()
    nazwa_ofert = zamowienie.nazwa_serwera
    dadatek = zamowienie.suma_netto - zamowienie.suma_netto_oferta
    nazwa_platnosc = zamowienie.rodzaj_platnosci
    suma_netto = zamowienie.suma_netto
    suma_brutto = zamowienie.suma_brutto

    podatek_vat = suma_brutto - suma_netto

    if dadatek == 0:
        dodatek = 'Brak dodatków'
    else:
        dodatek = '+ Dodatki'

    if fakturaa is True:
        faktura_nazwa = 'Wersja papierowa i elektroniczna'
    else:
        faktura_nazwa = 'Wersja elektroniczna'

    pay_nazwa = '%s %s' % (nazwa_ofert, dodatek)

    c = {'idt': idt, 'data_ter': data_ter, 'nazwa_ofert': nazwa_ofert, 'dodatek': dodatek, 'suma_netto': suma_netto,
         'suma_brutto': suma_brutto, 'podatek_vat': podatek_vat, 'nazwa_platnosc': nazwa_platnosc,
         'pay_nazwa': pay_nazwa, 'login_userr': login_userr, 'imie_me': imie_me, 'nazwisko_me': nazwisko_me,
         'email_me': email_me, 'faktura_nazwa': faktura_nazwa, 'telefonn': telefonn}
    return render_to_response("konto/zamowienie_paypal.html", c, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def pdf(request, kotern):
    z = Zamowienia.objects.get(user_id=request.user.id, id=kotern)
    # sprawdzam czy zamowienie jest zrealizowane
    if z.realizacja:

        # lokalny import - biblioteki dość spore szkoda pamięci RAM
        import StringIO
        from cgi import escape
        from xhtml2pdf import pisa
        from django.template import Context
        from django.template.loader import get_template
        from libs import liczba

        klient = RejestracjaKlienta.objects.get(user_id=request.user.id)

        data_wystawienia = z.data_zamowienia
        data_sprzedazy = z.data_zamowienia
        rodzaj_platnosci = z.rodzaj_platnosci
        nazwa_firmy = klient.nazwa_firmy
        # najlepiej w JS to zrobic zeby zapisywalo do bazy poprawnie
        nazwa_klienta = '%s%s %s%s' % (klient.imie[0].upper(), klient.imie[1:],
                                       klient.nazwisko[0].upper(), klient.nazwisko[1:])
        adres = '%s%s' % (klient.adres[0].upper(), klient.adres[1:])
        kod_pocztowy = klient.kod_pocztowy
        miasto = '%s%s' % (klient.miasto[0].upper(), klient.miasto[1:])
        nip = klient.nip
        regon = klient.regon
        dodatki_all = z.dodatki.all()

        try:
            nr_konta = KontaBankowe.objects.filter(konto_aktywne=True)[0]
        except IndexError:
            nr_konta = []

        nazwa_oferty = z.nazwa_serwera
        razem_netto = z.suma_netto
        razem_brutto = z.suma_brutto
        razem_slownie = liczba(razem_brutto)
        razem_vat = razem_brutto - razem_netto
        cena_netto_oferty = z.suma_netto_oferta
        cena_brutto_oferty = z.suma_brutto_oferta
        cena_vat_oferty = cena_brutto_oferty - cena_netto_oferty

        oferta = dict()
        oferta.update({'nazwa': nazwa_oferty, 'cena_netto': cena_netto_oferty, 'dodatek_vat': cena_vat_oferty,
                       'cena_brutto': cena_brutto_oferty})

        dodatki = []
        dodatki.append(oferta)
        for i in dodatki_all:
            dodatki.append(i.dodatki_id)

        nazwa_faktury = "FAKTURA VAT PROFORMA nr FVP/00%d/%s" % (z.id, z.date_added.year)

        context_dict = {'nazwa_faktury': nazwa_faktury, 'data_wystawienia': data_wystawienia, 'adres': adres,
                        'data_sprzedazy': data_sprzedazy, 'rodzaj_platnosci': rodzaj_platnosci, 'miasto': miasto,
                        'nazwa_firmy': nazwa_firmy, 'kod_pocztowy': kod_pocztowy, 'nip': nip, 'regon': regon,
                        'nazwa_oferty': nazwa_oferty, 'razem_netto': razem_netto, 'razem_brutto': razem_brutto,
                        'razem_vat': razem_vat, 'nr_konta': nr_konta, 'dodatki': dodatki, 'oferta': oferta,
                        'nazwa_klienta': nazwa_klienta, 'razem_slownie': razem_slownie}

        context_dict.update({'pagesize': 'A4'})

        template_name = "konto/faktura_vat.html"
        template = get_template(template_name)
        context = Context(context_dict)
        html = template.render(context)
        result = StringIO.StringIO()

        pisa.CreatePDF(html.encode("UTF-8"), result, encoding='UTF-8', link_callback=fetch_resources)

        try:
            response = HttpResponse(result.getvalue(), mimetype='application/pdf')

            # Enable if you want to generate pdf in a new file
            response['Content-Disposition'] = 'attachment; filename=%s.pdf' % \
                                              nazwa_faktury.replace(' ', '-').replace('/', '-')
            return response
        except:
            return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
    else:
        # jeżeli nie to zabezpieczam przed wpisaniem adresu do nieopłaconych (niewidocznych) faktur
        raise Http404


def fetch_resources(uri, rel):
    """ Access files and images."""
    import os
    path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    return path


@csrf_exempt
def kontakt(request):

    body_html = 'konto/formularz.html'
    body_html2 = 'konto/formularz_pomoc.html'

    if request.POST:
        kontakter = Kontakt(request.POST)

        kontakt = request.POST.get('kontakt')
        email = request.POST.get('email')
        temat = request.POST.get('temat')
        message = request.POST.get('message')

        html_content = render_to_string(body_html, {'kontakt': kontakt, 'email': email, 'temat': temat,
                                                    'message': message})
        text_content = strip_tags(html_content)

        html_content2 = render_to_string(body_html2, {'kontakt': kontakt, 'email': email, 'temat': temat,
                                                      'message': message})
        text_content2 = strip_tags(html_content2)

        if kontakter.is_valid():

            if kontakt == '1':

                subject = 'Formularz kontaktowy - Biuro Obsługi Klienta | SafeServer.pl'

                mail = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, ['biuro@safeserver.pl'])
                mail.attach_alternative(html_content, "text/html")
                mail.send()

                return HttpResponseRedirect('/kontakt/mail_wyslany/')
            else:

                subject = 'Formularz kontaktowy - Pomoc Techniczna | SafeServer.pl'

                mail = EmailMultiAlternatives(subject, text_content2, settings.EMAIL_HOST_USER, ['pomoc@safeserver.pl'])
                mail.attach_alternative(html_content2, "text/html")
                mail.send()

                return HttpResponseRedirect('/kontakt/mail_wyslany/')
    else:
        kontakter = Kontakt()

    return render_to_response("konto/kontakt.html", {'kontakter': kontakter}, context_instance=RequestContext(request))


@csrf_exempt
def kontakt_mail(request):
    return render_to_response("konto/mail_wyslany.html", context_instance=RequestContext(request))


@csrf_exempt
def onas(request):
    return render_to_response("konto/onas.html", context_instance=RequestContext(request))
