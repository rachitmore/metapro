from django.urls import path
from .views import pricing

app_name = 'pricing'

urlpatterns = [
    path('', pricing, name='pricing'),
]
