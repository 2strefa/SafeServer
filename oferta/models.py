#-*- encoding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from decimal import Decimal


class Koszyk(models.Model):

    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(default=datetime.datetime.now())
    user = models.ForeignKey(User, verbose_name=_('user'), null=True)
    oferta = models.IntegerField(null=True, blank=True)
    cena = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.0"))
    dodatki = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Total amount'), default=Decimal("0.0"))
    platnosc = models.IntegerField(null=True, blank=True, default=0)
    vat = models.PositiveIntegerField(verbose_name=_('VAT'), default=23)
    amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Total amount'), default=Decimal("0.0"), help_text=_('Without VAT'))
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Total amount'), default=Decimal("0.0"), help_text=_('Including VAT'))

    class Meta:
        db_table = 'Koszyk'
        verbose_name = 'Koszyk'
        verbose_name_plural = 'Koszyk'

    def __unicode__(self):
        return u"%s" % self.date_added


class Oferta(models.Model):
    nazwa = models.CharField(max_length=100, verbose_name=_('Nazwa oferty'), null=True, blank=True)
    cena_netto = models.DecimalField(max_digits=5, verbose_name=_('Cena netto za rok'), decimal_places=2)
    pojemnosc = models.CharField(max_length=100, null=True, blank=True)
    transfer = models.CharField(max_length=100, verbose_name=_('Transfer'), null=True, blank=True)
    baza_danych = models.CharField(max_length=100, null=True, blank=True)
    konta_pocztowe = models.CharField(max_length=100, verbose_name=_('Konta pocztowe'), null=True, blank=True)
    ftp = models.CharField(max_length=100, null=True, verbose_name=_('FTP'), blank=True)
    biblioteka = models.CharField(max_length=100, verbose_name=_('Biblioteka skryptow'), null=True, blank=True)
    quickinstall = models.BooleanField(default=False, verbose_name=_('QuickInstall'))
    kreator_www = models.BooleanField(default=False, verbose_name=_('Kreator www'))
    statystyki = models.BooleanField(default=False, verbose_name=_('Statystyki'))
    panel_cpanel = models.BooleanField(default=False, verbose_name=_('Panel cPanel'))
    konta_pocztowe_w_domenie = models.BooleanField(default=False)
    przekierowanie = models.BooleanField(default=False, verbose_name=_('Przekierowania poczty'))
    autoresponder = models.BooleanField(default=False, verbose_name=_('Autoresponder'))
    antyspam_antywirus = models.BooleanField(default=False, verbose_name=_('Antyspam i Antyvirus'))
    dostep_www = models.BooleanField(default=False)
    dostep_pop_imap = models.BooleanField(default=False, verbose_name=_('Dostep POP3/SMTP'))
    dostep_imap = models.BooleanField(default=False, verbose_name=_('Dostep przez IMAP'))
    multipoczta = models.BooleanField(default=False, verbose_name=_('Multipoczta'))
    poczta_mobilna = models.BooleanField(default=False, verbose_name=_('Poczta mobilna'))
    subdomeny = models.CharField(max_length=100, null=True, blank=True,verbose_name=_('Subdomeny'))
    cron = models.BooleanField(default=False, verbose_name=_('Harmonogram CRON'))
    ssl = models.BooleanField(default=False, verbose_name=_('Certyfikat SSL'))
    ssi = models.BooleanField(default=False, verbose_name=_('Server Side Includes (SSI)'))
    dziennik_serwera = models.BooleanField(default=False, verbose_name=_('Dziennik serwera'))
    ssh = models.BooleanField(default=False, verbose_name=_('SSH'))
    zabezpieczenie_strony_haslem = models.BooleanField(default=False)
    codzienna_kopia_bezpieczenstwa = models.BooleanField(default=False)
    php = models.BooleanField(default=False, verbose_name=_('PHP 5'))
    perl = models.BooleanField(default=False, verbose_name=_('Perl 5'))
    c_code = models.BooleanField(default=False, verbose_name=_('C'))
    c_plus_plus = models.BooleanField(default=False, verbose_name=_('C++'))
    xml = models.BooleanField(default=False, verbose_name=_('XML'))
    python = models.BooleanField(default=False, verbose_name=_('Python'))
    mod_rewire = models.BooleanField(default=False, verbose_name=_('mod_rewrite'))
    django = models.BooleanField(default=False, verbose_name=_('Django 1.4'))
    ruby_on_rails = models.BooleanField(default=False, verbose_name=_('Ruby on Rails'))
    licznik = models.BooleanField(default=False, verbose_name=_('Licznik'))
    formmail = models.BooleanField(default=False, verbose_name=_('Formmail'))
    redirected = models.BooleanField(default=False, verbose_name=_('Redirector'))
    gestbook = models.BooleanField(default=False, verbose_name=_('Guestbook'))
    search = models.BooleanField(default=False, verbose_name=_('Search'))

    class Meta:
        db_table = 'Oferta'
        verbose_name = 'Oferta'
        verbose_name_plural = 'Oferty'

    # def cena_brutto(self):
    #     return float(self.cena_netto) * 1.23

    # def vat(self):
    #     return self.cena_brutto() - float(self.cena_netto)

    def __unicode__(self):
        return u"%s" % self.nazwa


class Dodatki(models.Model):
    oferta_nazwa = models.ManyToManyField(Oferta, unique=False, verbose_name=_('Nazwa oferty'))
    nazwa = models.CharField(max_length=100, verbose_name=_('Nazwa dodatku'), null=True, blank=True)
    cena_netto = models.DecimalField(max_digits=5, verbose_name=_('Cena netto'), decimal_places=2)
    opis = models.TextField(null=True, blank=True, verbose_name=_('Opis'))

    class Meta:
        db_table = 'Dodatki'
        verbose_name = 'Dodatek'
        verbose_name_plural = 'Dodatki'

    # do obliczen
    def cena_brutto_digit(self):
        return float(self.cena_netto) * 1.23
    # tu juz tekst
    def cena_brutto(self):
        return "{:.2f}".format(float(self.cena_netto) * 1.23)

    def dodatek_vat(self):
        return "{:.2f}".format(self.cena_brutto_digit() - float(self.cena_netto))

    def __unicode__(self):
        return u"%s" % self.nazwa


class Dodatki_Id(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), unique=False, null=True, blank=True)
    cart_id = models.CharField(max_length=50, unique=False)
    dodatki_id = models.ForeignKey(Dodatki, verbose_name=_('Nazwa dodatku'), unique=False, null=True, blank=True)
    oferta_id = models.IntegerField(null=True, blank=True, verbose_name=_('Id oferty'))
    czas_dodatki = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'Dodatki_Id'
        verbose_name = 'Dodatek Id'
        verbose_name_plural = 'Dodatki Id'

    def __unicode__(self):
        return u"%s" % self.dodatki_id
