# trading/forms.py
from django import forms

class BacktestForm(forms.Form):
    symbol = forms.CharField(max_length=10)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    strategy_name = forms.CharField(max_length=50)
