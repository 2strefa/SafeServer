#-*- encoding: utf-8 -*-
import re
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings
from hashlib import sha1 as sha
import datetime
import calendar
import random
from django.utils.timezone import utc
from django.contrib.sites.models import Site
from paypal.standard.ipn.signals import payment_was_successful
from decimal import Decimal
from oferta.models import Dodatki_Id
# from django.utils.html import strip_tags
# from django.core.mail import EmailMultiAlternatives

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class RejestracjaKlienta(models.Model):

    user = models.ForeignKey(User, verbose_name=_('user'), null=True)
    jestem = models.IntegerField(verbose_name=_('Kim jestem'))
    imie = models.CharField(max_length=100, verbose_name=_('Imie'))
    nazwisko = models.CharField(max_length=100, verbose_name=_('Nazwisko'))
    adres = models.CharField(max_length=100, verbose_name=_('Adres'))
    miasto = models.CharField(max_length=100, verbose_name=_('Miasto'))
    kod_pocztowy = models.CharField(max_length=100, verbose_name=_('Kod pocztowy'))
    kraj = models.CharField(max_length=100, verbose_name=_('Kraj'))
    wojewodztwo = models.CharField(max_length=100, verbose_name=_('Wojewodztwo'), null=True, blank=True)
    telefon = models.CharField(max_length=100, verbose_name=_('Telefon'))
    telefon_dodatkowy = models.CharField(max_length=100, verbose_name=_('Telefon dodatkowy'), null=True, blank=True)
    nazwa_firmy = models.CharField(max_length=255, verbose_name=_('Nazwa firmy'), null=True, blank=True)
    nip = models.CharField(max_length=100, verbose_name=_('NIP'), null=True, blank=True)
    regon = models.CharField(max_length=100, verbose_name=_('REGON'), null=True, blank=True)
    faktura_vat = models.BooleanField(default=False, verbose_name=_('Faktura VAT'))
    newsletter = models.BooleanField(default=False, verbose_name=_('Newsletter'))
    regulamin = models.BooleanField(default=False, verbose_name=_('Regulamin serwisu'))


    class Meta:
        db_table = 'Rejestracja_Klienta'
        verbose_name = 'Rejestracja Klienta'
        verbose_name_plural = 'Rejestracja Klientów'

    def __unicode__(self):
        return u"%s" % self.imie

    def jestem_text(self):
        if self.jestem == 1:
            return 'Osoba Prywatna'
        else:
            return 'Firma'
    jestem_text.short_description = 'Typ klienta'
    # jestem_text.allow_tags = True


class RegistrationManager(models.Manager):

    def activate_user(self, activation_key):

        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                print 'activation key not expired'
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                return user
        return False

    def create_inactive_user(self, user, haslo, email, send_email=True, profile_callback=None):

        new_user = User.objects.create_user(user, email, haslo)
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user)

        if profile_callback is not None:
            profile_callback(user=new_user)

        if send_email:
            from django.core.mail import send_mail
            current_site = Site.objects.get_current()

            subject = render_to_string('konto/activation_email_subject.txt',
                                       {'site': current_site})

            subject = ''.join(subject.splitlines())

            message = render_to_string('konto/activation_email.txt',
                                       {'activation_key': registration_profile.activation_key,
                                         'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                                         'site': current_site})

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
        return new_user

    def create_profile(self, user):

        salt = sha(str(random.random())).hexdigest()[:5]
        activation_key = sha(salt+user.username).hexdigest()
        return self.create(user=user, activation_key=activation_key)

    def delete_expired_users(self):

        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()


class RegistrationProfile(models.Model):

    ACTIVATED = u"ALREADY_ACTIVATED"

    user = models.ForeignKey(User, related_name='user', unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)

    objects = RegistrationManager()

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')

    class Admin:
        list_display = ('__unicode__', 'activation_key_expired')
        search_fields = ('user__username', 'user__first_name')

    def __unicode__(self):
        return u"Registration information for %s" % self.user

    def activation_key_expired(self):

        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
            (self.user.date_joined + expiration_date <= datetime.datetime.utcnow().replace(tzinfo=utc))
    activation_key_expired.boolean = True


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    if ipn_obj.custom == "Upgrade all users!":
        User.objects.update(paid=True)
payment_was_successful.connect(show_me_the_money)


class Zamowienia(models.Model):

    cart_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, verbose_name=_('user'), unique=False)
    login = models.CharField(max_length=100, verbose_name=_('Login'))
    imie = models.CharField(max_length=100, verbose_name=_('Imie'))
    nazwisko = models.CharField(max_length=100, verbose_name=_('Nazwisko'))
    nazwa_serwera = models.CharField(max_length=100, verbose_name=_('Nazwa serwera'))
    numer_zamowienia = models.CharField(max_length=100, verbose_name=_('Numer zamowienia'), null=True, blank=True)
    data_zamowienia = models.CharField(max_length=100, verbose_name=_('Data zamowienia'), null=True, blank=True)
    data_waznosci = models.CharField(max_length=100, verbose_name=_('Data waznosci'), null=True, blank=True)
    rodzaj_platnosci = models.CharField(max_length=100, verbose_name=_('Rodzaj platnosci'), null=True, blank=True)
    suma_netto = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Suma netto'),
                                     default=Decimal("0.0"), help_text=_('Without VAT'))
    suma_brutto = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Suma brutto'),
                                      default=Decimal("0.0"), help_text=_('Including VAT'))
    suma_netto_oferta = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Suma netto oferty'),
                                            default=Decimal("0.0"), help_text=_('Without VAT'))
    suma_brutto_oferta = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Suma brutto oferty'),
                                             default=Decimal("0.0"), help_text=_('Including VAT'))
    realizacja = models.BooleanField(default=False, verbose_name=_('Realizacja zamowienia'))
    link_do_cpanelu = models.CharField(max_length=255, verbose_name=_('Link do CPanelu'), null=True, blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now())
    dodatki = models.ManyToManyField(Dodatki_Id, blank=True)

    class Meta:
        db_table = 'Zamowienia'
        verbose_name = 'Zamówienie'
        verbose_name_plural = 'Zamówienia'

    def __unicode__(self):
        return u"%s" % self.numer_zamowienia

    # metoda zwraca tuple [ilosc_dni, waznosc] konta
    def pozostalo_dni(self):
        now = datetime.datetime.today()
        waznosc = datetime.datetime.strptime(self.data_waznosci, '%d-%m-%Y')
        # pobieram dodatki zamowienia
        dodatki = self.dodatki.all()
        for i in dodatki:
            # pobieram kolejno id dodatkow
            dodatek = i.dodatki_id_id
            if dodatek in lista_id:
                waznosc = waznosc.replace(year=waznosc.year + 1)
                break
        ilosc_dni = waznosc - now
        return ilosc_dni.days, waznosc.strftime("%d-%m-%Y")
# lista id subskrypcji na serwerze produkcyjnym
lista_id = [11, 12, 13, 14]


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


class KontaBankowe(models.Model):
    nazwa_banku = models.CharField(max_length=100, verbose_name=_('Nazwa banku'))
    numer_konta = models.CharField(max_length=100, verbose_name=_('Numer konta'))
    konto_aktywne = models.BooleanField(verbose_name=_('Aktywne konto'), help_text=_('Jedno konto może być aktywne'))

    class Meta:
        verbose_name = 'Konto bankowe'
        verbose_name_plural = 'Konta bankowe'

    def __unicode__(self):
        return u"%s" % self.nazwa_banku
