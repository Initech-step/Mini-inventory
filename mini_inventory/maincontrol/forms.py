from django import forms
from django.db.models import fields
from .models import Inventories, Transactions

class CreateInventoryForm(forms.ModelForm):
    class Meta:
        model = Inventories
        fields = ('name', 'extra_notes', 'method_of_management')

class RecieveInventoryForm(forms.Form):
    quantity_recieved = forms.IntegerField(min_value=1)
    price = forms.FloatField()

class SendOutInventoryForm(forms.Form):
    quantity_sent_out = forms.IntegerField(min_value=1)