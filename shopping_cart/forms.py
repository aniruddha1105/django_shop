# shopping_cart/forms.py
from django import forms


class UpdateCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)
    action = forms.CharField(widget=forms.HiddenInput())
