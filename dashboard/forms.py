from django import forms
from .models import Transaction
from .models import WishlistItem
from django.contrib.auth.models import User

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude=('user',)
        fields = ['account', 'currency', 'category','amount','transaction_type','date','description']

class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['item_name', 'item_price']