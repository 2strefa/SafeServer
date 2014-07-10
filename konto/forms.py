# -*- coding: utf-8 -*-

import datetime

import time

import re

from django import forms

from django.utils.translation import ugettext_lazy as _

from django_countries.countries import COUNTRIES

from django.contrib.auth.models import User

from models import RejestracjaKlienta

from models import RegistrationProfile

alnum_re = re.compile(r'^\w+$')

KONTAKT = (('', ' ------------ Wybierz ------------ '),

                ('1', 'Biuro Obsługi Klienta'),

                ('2', 'Pomoc Techniczna'))

WOJEWODZTWO = (('', ' ------------- Wybierz ------------- '),

                ('dolnośląskie', 'dolnośląskie'),

                ('kujawsko-pomorskie', 'kujawsko-pomorskie'),

                ('lubelskie', 'lubelskie'),

                ('lubuskie', 'lubuskie'),

                ('łódzkie', 'łódzkie'),

                ('małopolskie', 'małopolskie'),

                ('mazowieckie', 'mazowieckie'),

                ('opolskie', 'opolskie'),

                ('podkarpackie', 'podkarpackie'),

                ('podlaskie', 'podlaskie'),

                ('pomorskie', 'pomorskie'),

                ('śląskie', 'śląskie'),

                ('świętokrzyskie', 'świętokrzyskie'),

                ('warmińsko-mazurskie', 'warmińsko-mazurskie'),

                ('wielkopolskie', 'wielkopolskie'),

                ('zachodniopomorskie', 'zachodniopomorskie'))


class LoginForm(forms.Form):

    login_panel = forms.CharField(max_length=264, required=True, error_messages={'required': 'Musisz podać swój indywidualny login.'}, label=_(u'Login'))

    haslo_panel = forms.CharField(required=True, error_messages={'required': 'Musisz podać prawidłowe hasło do konta.'}, widget=forms.PasswordInput( render_value=False), label=_(u'password'))


class RejestracjaUsera(forms.ModelForm):

    CHOICES=[('1','Jestem Osobą Prywatną'),('2','Jestem Firmą')]
    jestem = forms.ChoiceField(required=True, choices=CHOICES, widget=forms.RadioSelect(), error_messages={'required': 'Musisz wybrać Kim jesteś.'})

    login = forms.CharField(max_length=264, required=True, error_messages={'required': 'Musisz podać Swój indywidualny login.'},widget=forms.TextInput(attrs={'class':'input_klik'}))

    first_name = forms.CharField(required=True, max_length=30, error_messages={'required': 'Musisz podać Swoje Imię.'}, widget=forms.TextInput(attrs={'class':'input_klik'}))

    last_name = forms.CharField(required=True, max_length=30, error_messages={'required': 'Musisz podać Swoje Nazwisko.'}, widget=forms.TextInput(attrs={'class':'input_klik'}))

    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'input_klik'}))

    password1 = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False), error_messages={'required': 'Musisz podać hasło.'})

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False), error_messages={'required': 'Musisz powtórzyć Swoje hasło.'})

    adres = forms.CharField(max_length=140, required=True, widget=forms.TextInput(attrs={'class':'input_klik'}), error_messages={'required': 'Musisz podać Swój adres.'})

    miasto = forms.CharField(max_length=40, required=True, widget=forms.TextInput(attrs={'class':'input_klik'}), error_messages={'required': 'Musisz podać Swoje miasto.'})

    kod_pocztowy = forms.CharField(max_length=40, required=True, widget=forms.TextInput(attrs={'class':'input_klik'}), error_messages={'required': 'Musisz podać Swój kod pocztowy.'})

    kraj = forms.ChoiceField(required=True, choices=COUNTRIES, error_messages={'required': 'Musisz wybrać Swój kraj.'})

    wojewodztwo = forms.ChoiceField(required=False, choices=WOJEWODZTWO)

    phone = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class':'input_klik'}), error_messages={'required': 'Musisz podać Swój numer telefonu do kontaktu.'})

    dodatkow_tel = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class':'input_klik'}))

    pelnanazwafirmy = forms.CharField(max_length=264, required=False, widget=forms.TextInput(attrs={'class':'input_klik'}))

    nip = forms.CharField(max_length=40, required=False, widget=forms.TextInput(attrs={'class':'input_klik'}))

    regon = forms.CharField(max_length=40, required=False, widget=forms.TextInput(attrs={'class':'input_klik'}))

    akceptacja_vat = forms.BooleanField(required=False, widget=forms.CheckboxInput)

    chce_newsletter = forms.BooleanField(required=False,initial=True, widget=forms.CheckboxInput)

    akc_regul = forms.BooleanField(required=True, error_messages={'required': 'Aby się zarejestrować, musisz zaakceptować regulamin.'}, widget=forms.CheckboxInput)

    class Meta:
        model = RejestracjaKlienta
        fields = ['jestem','login','first_name','last_name','email','password1','adres','miasto','kod_pocztowy','kraj','wojewodztwo','phone','dodatkow_tel','pelnanazwafirmy','nip','regon','akceptacja_vat','chce_newsletter','akc_regul']

    def clean_login(self):

        if not alnum_re.search(self.cleaned_data['login']):
            raise forms.ValidationError(_(u'Login może zawierać, tylko cyfru, litery i podkreślenia.'))
        try:
            User.objects.get(username__iexact=self.cleaned_data['login'])
        except User.DoesNotExist:
            return self.cleaned_data['login']
        raise forms.ValidationError(_(u'Ten login jest już zajęty. Prosimy o wybranie innego.'))

    def clean_email(self):

        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_(u'Ten adres email jest już zajęty. Prosimy o wybranie innego.'))

    def clean(self):

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data


    def save(self, profile_callback=None):

        new_user = RegistrationProfile.objects.create_inactive_user(user=self.cleaned_data['login'], haslo=self.cleaned_data['password1'], email=self.cleaned_data['email'], profile_callback=profile_callback)

        new_profile = RejestracjaKlienta(user=new_user, jestem=self.cleaned_data['jestem'], imie=self.cleaned_data['first_name'], nazwisko=self.cleaned_data['last_name'], adres=self.cleaned_data['adres'], miasto=self.cleaned_data['miasto'],
                                          kod_pocztowy=self.cleaned_data['kod_pocztowy'], kraj=self.cleaned_data['kraj'], wojewodztwo=self.cleaned_data['wojewodztwo'], telefon=self.cleaned_data['phone'],
                                          telefon_dodatkowy=self.cleaned_data['dodatkow_tel'], nazwa_firmy=self.cleaned_data['pelnanazwafirmy'], nip=self.cleaned_data['nip'], regon=self.cleaned_data['regon'],
                                          faktura_vat=self.cleaned_data['akceptacja_vat'], newsletter=self.cleaned_data['chce_newsletter'], regulamin=self.cleaned_data['akc_regul'])

        new_profile.save()

        return new_user

class PlatnoscKlienta(forms.Form):

    CHOICES=[('1','Przelewy24.pl'),('2','PayPal'),('3','Przelew Zwykły')]
    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

class RealizacjaZamowienia(forms.Form):

    login = forms.CharField(required=True, max_length=264)
    nazwa_serwera = forms.CharField(required=True, max_length=264)
    imie = forms.CharField(required=True, max_length=264)
    nazwisko = forms.CharField(required=True, max_length=264)
    dodatki = forms.CharField(required=True, max_length=264)
    rodzaj_platnosci = forms.CharField(required=True, max_length=264)
    suma_netto = forms.CharField(required=True, max_length=264)
    suma_brutto = forms.CharField(required=True, max_length=264)
    numer_zamowienia = forms.CharField(required=True, max_length=264)
    data_zamowienia = forms.CharField(required=True, max_length=264)

class Kontakt(forms.Form):

    kontakt = forms.ChoiceField(required=True, choices=KONTAKT, error_messages={'required': 'Należy wybrać dział obsługi do kontaktu.'})
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'input_klikok'}), error_messages={'required': 'Pole E-mail jest wymagane.'})
    temat = forms.CharField(required=True, max_length=264, widget=forms.TextInput(attrs={'class':'input_klikok'}), error_messages={'required': 'Pole tematu jest wymagane.'})
    message = forms.CharField(required=True, widget=forms.Textarea, error_messages={'required': 'Pole wiadomości jest wymagane.'})