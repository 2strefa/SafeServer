from django import forms
from models import Koszyk, Dodatki
from oferta.models import Oferta
from django.forms import ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

class OfertaForm(forms.ModelForm):

    class Meta:
        model = Koszyk
        fields = ['oferta','cena']

class DodatkiForms(forms.ModelForm):

    pik = forms.ModelMultipleChoiceField(queryset=Oferta.objects.get(id=2).dodatki_set.all().order_by('nazwa'), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Dodatki
        fields = ['nazwa','cena_netto']

class DodatkiForms2(forms.ModelForm):

    pik = forms.ModelMultipleChoiceField(queryset=Oferta.objects.get(id=3).dodatki_set.all().order_by('nazwa'), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Dodatki
        fields = ['nazwa','cena_netto']

class DodatkiForms3(forms.ModelForm):

    pik = forms.ModelMultipleChoiceField(queryset=Oferta.objects.get(id=4).dodatki_set.all().order_by('nazwa'), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Dodatki
        fields = ['nazwa','cena_netto']

class DodatkiForms4(forms.ModelForm):

    pik = forms.ModelMultipleChoiceField(queryset=Oferta.objects.get(id=4).dodatki_set.all().order_by('nazwa'), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Dodatki
        fields = ['nazwa','cena_netto']


class DodatekKosz(forms.ModelForm):

    class Meta:
        model = Koszyk
        fields = ['dodatki','amount','total_amount']