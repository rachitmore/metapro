# trading/urls.py
from django.urls import path
from .views import backtest

app_name = 'trading_strategies' 

urlpatterns = [
    path('', backtest, name='backtest'),
]
