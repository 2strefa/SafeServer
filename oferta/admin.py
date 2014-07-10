#-*- encoding: utf-8 -*-
from django.contrib import admin
from models import Oferta, Dodatki

class OfertaAdmin(admin.ModelAdmin):

    list_display = ('nazwa','cena_netto','pojemnosc','transfer','baza_danych','konta_pocztowe','ftp','biblioteka','quickinstall','kreator_www','statystyki','panel_cpanel','konta_pocztowe_w_domenie','przekierowanie','autoresponder','antyspam_antywirus','dostep_www','dostep_pop_imap','dostep_imap','multipoczta','poczta_mobilna','subdomeny','cron','ssl','ssi','dziennik_serwera','ssh','zabezpieczenie_strony_haslem','codzienna_kopia_bezpieczenstwa','php','perl','c_code','c_plus_plus','xml','python','mod_rewire','django','ruby_on_rails','licznik','formmail','redirected','gestbook','search')

    list_display_links = ['nazwa','cena_netto']

    search_fields = ['nazwa','cena_netto']

admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Dodatki)
