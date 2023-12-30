from django.urls import path
from .views import home

app_name = 'about_us'

urlpatterns = [
    path('', home, name='home'),
]
