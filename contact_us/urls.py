# contactus/urls.py
from django.urls import path
from .views import contact_us, contact_us_success

app_name = 'contact_us'

urlpatterns = [
    path('contact-us/', contact_us, name='contact_us'),
    path('contact-us/success/', contact_us_success, name='contact_us_success'),
]
