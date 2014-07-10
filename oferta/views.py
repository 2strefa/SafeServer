from django.shortcuts import  render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.sessions.models import Session
import random
# from django.contrib.sessions.backends.db import SessionStore
# from importlib import import_module
# from django.conf import settings
# from django.contrib.auth.models import User
# import json
# import math
import datetime
from django.core import serializers
# from django.forms.models import modelformset_factory
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required
# from decimal import Decimal
from forms import OfertaForm, DodatkiForms, DodatekKosz, DodatkiForms2, DodatkiForms3, DodatkiForms4
from konto.forms import LoginForm
# from django.contrib.auth.models import User
from models import Koszyk, Dodatki, Oferta, Dodatki_Id
from konto.models import RejestracjaKlienta



# from django.utils import timezone



CART_ID_SESSION_KEY = 'cart_id'

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


def hosting(request):

    return render_to_response('oferta/hosting.html', context_instance=RequestContext(request))


def starter(request):

    if request.POST:

        formator = OfertaForm(request.POST)

        if formator.is_valid():

            oferta = request.POST.get('oferta')
            cena = request.POST.get('cena')
            d, create = Koszyk.objects.get_or_create(cart_id=_cart_id(request))
            d.date_added = datetime.datetime.now()
            d.user_id = request.user.id
            d.oferta = oferta
            d.cena = cena
            d.save()

            return HttpResponseRedirect('/hosting/starter/dodatki/')

    else:

        formator = OfertaForm()

    c = {'form': formator}
    c.update(csrf(request))

    return render_to_response('oferta/starter.html', c, context_instance=RequestContext(request))


def standard(request):

    if request.POST:

        formator = OfertaForm(request.POST)

        if formator.is_valid():

            oferta = request.POST.get('oferta')
            cena = request.POST.get('cena')
            d, create = Koszyk.objects.get_or_create(cart_id=_cart_id(request))
            d.date_added = datetime.datetime.now()
            d.user_id = request.user.id
            d.oferta = oferta
            d.cena = cena
            d.save()

            return HttpResponseRedirect('/hosting/standard/dodatki/')

    else:

        formator = OfertaForm()

    c = {'form':formator}
    c.update(csrf(request))

    return render_to_response('oferta/standard.html', c , context_instance=RequestContext(request))



def buisness(request):

    if request.POST:

        formator = OfertaForm(request.POST)

        if formator.is_valid():

            oferta = request.POST.get('oferta')
            cena = request.POST.get('cena')
            d, create = Koszyk.objects.get_or_create(cart_id=_cart_id(request))
            d.date_added = datetime.datetime.now()
            d.user_id = request.user.id
            d.oferta = oferta
            d.cena = cena
            d.save()

            return HttpResponseRedirect('/hosting/business/dodatki/')
    else:

        formator = OfertaForm()

    c = {'form':formator}
    c.update(csrf(request))

    return render_to_response('oferta/buisness.html', c ,context_instance=RequestContext(request))


def pro(request):

    if request.POST:

        formator = OfertaForm(request.POST)

        if formator.is_valid():
            oferta = request.POST.get('oferta')
            cena = request.POST.get('cena')
            d, create = Koszyk.objects.get_or_create(cart_id=_cart_id(request))
            d.date_added = datetime.datetime.now()
            d.user_id = request.user.id
            d.oferta = oferta
            d.cena = cena
            d.save()

            return HttpResponseRedirect('/hosting/professional/dodatki/')

    else:

        formator = OfertaForm()

    c = {'form':formator}
    c.update(csrf(request))

    return render_to_response('oferta/pro.html',c, context_instance=RequestContext(request))


def json_start(request):

    queryset = Dodatki.objects.all()
    serial_ter = serializers.serialize("json", queryset, indent=4)
    data_json = serial_ter.decode("unicode_escape").encode("utf8")
    return HttpResponse(data_json, mimetype='application/json')


def json_oferta(request):

    queryset = Oferta.objects.all()
    serial_ter = serializers.serialize("json", queryset, indent=4)
    data_json = serial_ter.decode("unicode_escape").encode("utf8")
    return HttpResponse(data_json, mimetype='application/json')


def dodatki_starter(request):
       
    formset = DodatkiForms()
    projekt = Oferta.objects.get(id=2).dodatki_set.all().order_by('nazwa')
    myCheckboxess = request.POST.getlist('pik[]')
    placer = Oferta.objects.get(id=2).dodatki_set.all().order_by('nazwa')
    prok = sum([i.cena_netto for i in placer])
    oferta_netto = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
    oferte_cena = oferta_netto.cena

    data_koszyk = oferta_netto.date_added

    if request.POST:

        formset2 = DodatekKosz(request.POST)

        if formset2.is_valid():

            dada = request.POST.get('dodatki')
            nettor = request.POST.get('amount')
            razem_ty = request.POST.get('total_amount')
            metodaplacty = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
            metodaplacty.dodatki = dada
            metodaplacty.amount = nettor
            metodaplacty.total_amount = razem_ty
            metodaplacty.save()

            list = request.POST.getlist('pik')

            pikert = [int(i) for i in list]
            for i in pikert:
                g = Dodatki_Id.objects.create(cart_id=_cart_id(request))
                g.dodatki_id_id = i
                g.oferta_id = 2
                g.czas_dodatki = data_koszyk
                g.save()

            return HttpResponseRedirect('/weryfikacja_klienta/')

    else:
        
        formset2 = DodatekKosz()

    c = {'items':formset,'formt2':formset2, 'qter':projekt, 'cena':placer, 'myCheckboxes':myCheckboxess}
    c.update(csrf(request))

    return render_to_response('oferta/dodatki.html',c,context_instance=RequestContext(request))


def dodatki_standard(request):

    formset = DodatkiForms2()
    projekt = Oferta.objects.get(id=3).dodatki_set.all().order_by('nazwa')
    myCheckboxess = request.POST.getlist('pik[]')
    placer = Oferta.objects.get(id=3).dodatki_set.all().order_by('nazwa')
    prok = sum([i.cena_netto for i in placer])
    oferta_netto = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
    oferte_cena = oferta_netto.cena

    data_koszyk = oferta_netto.date_added

    if request.POST:

        formset2 = DodatekKosz(request.POST)

        if formset2.is_valid():

            dada = request.POST.get('dodatki')
            nettor = request.POST.get('amount')
            razem_ty = request.POST.get('total_amount')
            metodaplacty = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
            metodaplacty.dodatki = dada
            metodaplacty.amount = nettor
            metodaplacty.total_amount = razem_ty
            metodaplacty.save()

            # komentarz w 'dodatki_starter'
            list = request.POST.getlist('pik')
            pikert = [int(i) for i in list]
            # Dodatki_Id.objects.filter(cart_id=_cart_id(request)).delete()
            for i in pikert:
                g = Dodatki_Id.objects.create(cart_id=_cart_id(request))
                # g.user_id = request.user.id
                g.dodatki_id_id = i
                g.oferta_id = 3
                g.czas_dodatki = data_koszyk
                g.save()

            return HttpResponseRedirect('/weryfikacja_klienta/')

    else:
        formset2 = DodatekKosz()

    c = {'items':formset,'formt2':formset2, 'qter':projekt, 'cena':placer, 'myCheckboxes':myCheckboxess}
    c.update(csrf(request))

    return render_to_response('oferta/dodatki_standard.html',c, context_instance=RequestContext(request))



def dodatki_business(request):

    formset = DodatkiForms3()
    projekt = Oferta.objects.get(id=4).dodatki_set.all().order_by('nazwa')
    myCheckboxess = request.POST.getlist('pik[]')
    placer = Oferta.objects.get(id=4).dodatki_set.all().order_by('nazwa')
    prok = sum([i.cena_netto for i in placer])
    oferta_netto = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
    oferte_cena = oferta_netto.cena

    data_koszyk = oferta_netto.date_added

    if request.POST:

        formset2 = DodatekKosz(request.POST)

        if formset2.is_valid():

            dada = request.POST.get('dodatki')
            nettor = request.POST.get('amount')
            razem_ty = request.POST.get('total_amount')
            metodaplacty = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
            metodaplacty.dodatki = dada
            metodaplacty.amount = nettor
            metodaplacty.total_amount = razem_ty
            metodaplacty.save()

            # komentarz w 'dodatki_starter'
            list = request.POST.getlist('pik')
            pikert = [int(i) for i in list]
            for i in pikert:
                g = Dodatki_Id.objects.create(cart_id=_cart_id(request))
                g.dodatki_id_id = i
                g.oferta_id = 4
                g.czas_dodatki = data_koszyk
                g.save()

            return HttpResponseRedirect('/weryfikacja_klienta/')
    else:
        formset2 = DodatekKosz()

    c = {'items': formset, 'formt2': formset2, 'qter':projekt, 'cena':placer, 'myCheckboxes':myCheckboxess}
    c.update(csrf(request))

    return render_to_response('oferta/dodatki_buisness.html', c, context_instance=RequestContext(request))



def dodatki_professional(request):

    formset = DodatkiForms4()
    projekt = Oferta.objects.get(id=4).dodatki_set.all().order_by('nazwa')
    myCheckboxess = request.POST.getlist('pik[]')
    placer = Oferta.objects.get(id=4).dodatki_set.all().order_by('nazwa')
    prok = sum([i.cena_netto for i in placer])
    oferta_netto = Koszyk.objects.get(cart_id=_cart_id(request))
    oferte_cena = oferta_netto.cena

    data_koszyk = oferta_netto.date_added

    if request.POST:

        formset2 = DodatekKosz(request.POST)

        if formset2.is_valid():

            dada = request.POST.get('dodatki')
            nettor = request.POST.get('amount')
            razem_ty = request.POST.get('total_amount')
            metodaplacty = Koszyk.objects.get(cart_id=_cart_id(request), user_id=request.user.id)
            metodaplacty.dodatki = dada
            metodaplacty.amount = nettor
            metodaplacty.total_amount = razem_ty
            metodaplacty.save()

            # komentarz w 'dodatki_starter'
            list = request.POST.getlist('pik')
            pikert = [int(i) for i in list]
            for i in pikert:
                g = Dodatki_Id.objects.create(cart_id=_cart_id(request))
                g.dodatki_id_id = i
                g.oferta_id = 4
                g.czas_dodatki = data_koszyk
                g.save()

            return HttpResponseRedirect('/weryfikacja_klienta/')
    else:
        formset2 = DodatekKosz()

    c = {'items': formset, 'formt2': formset2, 'qter': projekt, 'cena': placer, 'myCheckboxes': myCheckboxess}
    c.update(csrf(request))

    return render_to_response('oferta/dodatki_pro.html',c ,context_instance=RequestContext(request))



def weryfikacja(request):

    aktywny_er = RejestracjaKlienta.objects.filter(user_id=request.user.id)


    for e in aktywny_er:

        koala = e.user

        if koala is not None:

            return HttpResponseRedirect('/zweryfikowany/')

    if request.POST:

        form = LoginForm(request.POST)

        logowanie = request.POST.get('login_panel', '')
        haslowanie = request.POST.get('haslo_panel', '')



        if form.is_valid():

                user_sprzed = auth.authenticate(username=logowanie, password=haslowanie)

                if user_sprzed is not None:

                    auth.login(request, user_sprzed)
                    return HttpResponseRedirect('/zweryfikowany/')

    else:

        form = LoginForm()

    c = {'form': form}
    c.update(csrf(request))



    return render_to_response('konto/weryfikacja.html',c, context_instance=RequestContext(request))





