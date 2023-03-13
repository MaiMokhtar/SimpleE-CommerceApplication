from django import forms

from shopping.models import Item


class PurchaseForm(forms.Form):
    """A form for selecting items to purchase.

    Attributes:
        items: A ModelMultipleChoiceField representing the items available for purchase.

    """
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.CheckboxSelectMultiple())
