from django import forms
from logic.models import *


class changeInfoForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'
        exclude = ['person']


class buyTovar(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['count']
