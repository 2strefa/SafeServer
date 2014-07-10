from django.conf.urls import *

from django.conf import settings

from konto.views import activate
from konto.views import register
# from konto.views import pdf

# from django.conf.urls.static import static

from django.contrib.auth.views import *

from django.views.generic import TemplateView

# from django.contrib.auth import views as auth_views

# from django.contrib.auth.decorators import login_required

# from django.views.decorators.csrf import csrf_exempt

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'home.views.index', name='home_index'),

    url(r'^okres-testowy/$', 'home.views.okres_testowy', name='okres_testowy'),

    url(r'^przeniesienie-hostingu/$', 'home.views.przeniesienie_hostingu', name='przeniesienie_hostingu'),

    url(r'^onas/$', 'konto.views.onas', name='onas_index'),

    url(r'^login/$', 'konto.views.login', name='login_index'),

    url(r'^wylogowanie/$', logout,{'template_name': 'base.html'}, name='home_logout'),

    url(r'^regulaminy/$', 'home.views.regulamin', name='regulamin_index'),

    url(r'^hosting/$', 'oferta.views.hosting', name='hosting_index'),

    url(r'^hosting/starter/$', 'oferta.views.starter', name='oferta_starter'),

    url(r'^hosting/standard/$', 'oferta.views.standard', name='oferta_standard'),

    url(r'^hosting/business/$', 'oferta.views.buisness', name='oferta_buisness'),

    url(r'^hosting/professional/$', 'oferta.views.pro', name='oferta_pro'),

    url(r'^rejestracja/$', 'konto.views.register', name='rejestracja_index'),

    url(r'^hosting/starter/dodatki/$', 'oferta.views.dodatki_starter', name='oferta_dodatki_starter'),

    url(r'^hosting/standard/dodatki/$', 'oferta.views.dodatki_standard', name='oferta_dodatki_standard'),

    url(r'^hosting/business/dodatki/$', 'oferta.views.dodatki_business', name='oferta_dodatki_business'),

    url(r'^hosting/professional/dodatki/$', 'oferta.views.dodatki_professional', name='oferta_dodatki_professional'),

    url(r'^ajax_starter/$', 'oferta.views.json_start', name='ajax_starter'),

    url(r'^ajax_oferta/$', 'oferta.views.json_oferta', name='ajax_oferta'),

    url(r'^weryfikacja_klienta/$', 'oferta.views.weryfikacja', name='weryfikacja'),

    url(r'^zweryfikowany/$', 'konto.views.daneklienta_koszy', name='dane_klienta_koszyk'),

    url(r'^konto_klienta/$', 'konto.views.konto', name='konto_index'),

    url(r'^platnosc/$', 'konto.views.platnosc', name='platnosc_index'),

    url(r'^kontakt/$', 'konto.views.kontakt', name='kontakt_index'),

    url(r'^kontakt/mail_wyslany/$', 'konto.views.kontakt_mail', name='kontakt_mail_index'),

    url(r'^podsumowanie_przelewy24/$', 'konto.views.podsumowanie_przelewy24', name='podsumowanie_przelewy24_index'),

    url(r'^podsumowanie_paypal/$', 'konto.views.podsumowanie_paypal', name='podsumowanie_paypal_index'),

    url(r'^podsumowanie_przelew_zwykly/$', 'konto.views.podsumowanie_przelew', name='podsumowanie_przelew_index'),

    url(r'^moj_ipn/$', include('paypal.standard.ipn.urls')),

    url(r'^konto_klienta/pdf/(?P<kotern>\d+)/$', 'konto.views.pdf', name='pdf_index'),

    url(r'^konto_klienta/platnosc_paypal_zaakceptowana/$', 'konto.views.platnoscpaypalzaakceptowana', name='paypal_akceptacja_index'),

    url(r'^konto_klienta/platnosc_paypal_odrzucona/$', 'konto.views.platnoscpaypalodrzucona', name='paypal_odrzucona_index'),

    url(r'^konto_klienta/zamowienie_przelew/$', 'konto.views.zamowienieprzelew', name='zamowienie_przelew_index'),

    url(r'^konto_klienta/zamowienie_przelew/(?P<slug>\d+)/$', 'konto.views.zamowienieprzelew_zestawienie', name='zamowienie_przelew_zestawienie_index'),

    url(r'^konto_klienta/zamowienie_paypal/$', 'konto.views.zamowieniepaypal', name='zamowienie_paypal_index'),

    url(r'^konto_klienta/zamowienie_paypal/(?P<slug>\d+)/$', 'konto.views.zamowieniepaypal_zestawienie', name='zamowienie_paypal_zestawienie_index'),


    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^projekt2strefa/', include(admin.site.urls)),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^aktywacja/(?P<activation_key>\w+)/$', activate, name='registration_activate'),

    url(r'^rejestracja/$', register, name='registration_register'),

    url(r'^rejestracja/zakonczona/$', TemplateView.as_view(template_name='konto/rejestracja_zakonczona.html'), name='registration_end'),

)
