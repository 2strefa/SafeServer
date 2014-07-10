#-*- encoding: utf-8 -*-
from django.contrib import admin
# import datetime
# from django.contrib import messages
from models import Zamowienia, RejestracjaKlienta, KontaBankowe
from oferta.models import Koszyk, Dodatki_Id
from django.contrib.auth.models import User
from safeserver.settings import EMAIL_HOST_USER as email_host
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from django.utils.translation import ugettext as _
# from django.utils.encoding import force_unicode
# from django.http import HttpResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse

class KontaBankoweAdmin(admin.ModelAdmin):

    list_display = ('nazwa_banku', 'numer_konta', 'konto_aktywne')

admin.site.register(KontaBankowe, KontaBankoweAdmin)

class ZamowieniaAdmin(admin.ModelAdmin):
    # wywalam date picker bo usuwa mikrosekundy przy zapisie
    exclude = ('date_added',)
    list_display = ('numer_zamowienia', 'data_zamowienia', 'login', 'imie', 'nazwisko', 'nazwa_serwera',
                    'data_waznosci', 'rodzaj_platnosci', 'suma_netto', 'suma_brutto', 'realizacja', 'link_do_cpanelu')
    list_display_links = ['numer_zamowienia']
    search_fields = ['numer_zamowienia', 'data_zamowienia', 'imie', 'nazwisko', 'nazwa_serwera', 'data_waznosci']

    def save_model(self, request, obj, form, change):
        print
        if 'realizacja' in form.changed_data:
            user = User.objects.get(username=obj.user)
            klient = RejestracjaKlienta.objects.get(user_id=user.id)
            email_me = user.email
            numer_zamowienia = obj.numer_zamowienia
            data_zamowienia = obj.data_zamowienia
            login = obj.login
            imie = obj.imie
            nazwisko = obj.nazwisko
            rodzaj_platnosci = obj.rodzaj_platnosci

            adress = klient.adres
            kod_pocztek = klient.kod_pocztowy
            miastoo = klient.miasto
            krajj = klient.kraj
            telefonn_dodat = klient.telefon_dodatkowy
            nazwa_firmyy = klient.nazwa_firmy
            nip_fir = klient.nip
            regon_fir = klient.regon
            imie_firmy = klient.nazwa_firmy

            cart_id = obj.cart_id
            data_koszyk = obj.date_added

            d = Dodatki_Id.objects.filter(cart_id=cart_id, czas_dodatki=data_koszyk)
            list_dodatki = []
            for i in d:
                list_dodatki.append(i.dodatki_id.nazwa)

            pay_nazwa = obj.nazwa_serwera

            body_html = 'konto/informacja_o_aktywacji_do_klienta.html'

            if obj.realizacja:

                text1 = 'Dziękujemy za dokonanie zakupów na Safeserver.pl'
                text2 = 'Konto zostało aktywowane.'

                html_content = render_to_string(body_html, {
                    'numer_zamowienia': numer_zamowienia, 'data_zamowienia': data_zamowienia, 'login': login,
                    'email_me': email_me, 'imie': imie, 'nazwisko': nazwisko, 'adress': adress, 'kod_pocztek': kod_pocztek,
                    'miastoo': miastoo, 'kraj': krajj, 'telefonn_dodat': telefonn_dodat, 'nazwa_firmyy': nazwa_firmyy,
                    'nip_fir': nip_fir, 'regon_fir': regon_fir, 'imie_firmy': imie_firmy,
                    'rodzaj_platnosci': rodzaj_platnosci, 'pay_nazwa': pay_nazwa, 'list_dodatki': list_dodatki,
                    'text1': text1, 'text2': text2
                })
                text_content = strip_tags(html_content)

                subject = u'Automatyczny e-mail o zaakceptowaniu płatności - Zamówienie nr %s' % numer_zamowienia
                mail = EmailMultiAlternatives(subject, text_content, email_host, [email_me])
                mail.attach_alternative(html_content, "text/html")
                mail.send()
            else:

                text1 = 'Prosimy o opłacenie zamówienia.'
                text2 = 'Konto zostało zablokowane.'

                html_content = render_to_string(body_html, {
                    'numer_zamowienia': numer_zamowienia, 'data_zamowienia': data_zamowienia, 'login': login,
                    'email_me': email_me, 'imie': imie, 'nazwisko': nazwisko, 'adress': adress, 'kod_pocztek': kod_pocztek,
                    'miastoo': miastoo, 'kraj': krajj, 'telefonn_dodat': telefonn_dodat, 'nazwa_firmyy': nazwa_firmyy,
                    'nip_fir': nip_fir, 'regon_fir': regon_fir, 'imie_firmy': imie_firmy,
                    'rodzaj_platnosci': rodzaj_platnosci, 'pay_nazwa': pay_nazwa, 'list_dodatki': list_dodatki,
                    'text1': text1, 'text2': text2
                })
                text_content = strip_tags(html_content)

                subject = u'Automatyczny e-mail o niepłaconym zamówieniu - Zamówienie nr %s' % numer_zamowienia
                mail = EmailMultiAlternatives(subject, text_content, email_host, [email_me])
                mail.attach_alternative(html_content, "text/html")
                mail.send()
        admin.ModelAdmin.save_model(self, request, obj, form, change)

admin.site.register(Zamowienia, ZamowieniaAdmin)

class KoszykAdmin(admin.ModelAdmin):
    # wywalam date picker bo usuwa mikrosekundy przy zapisie
    exclude = ('date_added',)
    list_display = ('date_added', 'cart_id', 'user', 'oferta', 'cena', 'dodatki', 'platnosc', 'vat', 'amount',
                    'total_amount')
    list_display_links = ['date_added']
    search_fields = ['date_added', 'cart_id', 'user', 'oferta', 'cena', 'dodatki', 'platnosc', 'vat', 'amount',
                     'total_amount']

admin.site.register(Koszyk, KoszykAdmin)

class RejestracjaAdmin(admin.ModelAdmin):

    list_display = ('jestem_text', 'imie', 'nazwisko', 'adres', 'miasto', 'kod_pocztowy', 'kraj', 'wojewodztwo',
                    'telefon', 'telefon_dodatkowy', 'nazwa_firmy', 'nip', 'regon', 'faktura_vat', 'newsletter',
                    'regulamin')
    list_display_links = ['imie', 'nazwisko']
    search_fields = ['jestem', 'imie', 'nazwisko', 'adres', 'miasto', 'kod_pocztowy', 'kraj', 'wojewodztwo', 'telefon',
                     'telefon_dodatkowy', 'nazwa_firmy', 'nip', 'regon']

admin.site.register(RejestracjaKlienta, RejestracjaAdmin)
