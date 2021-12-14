from django.urls import path, include
from website.views import get_sto, put_sto, get_month_year

urlpatterns = [
    path('sto/', get_sto),
    path('create-sto/', put_sto),
    path('test/', get_month_year),
]