from django.urls import path, include
from website.views import get_sto, put_sto

urlpatterns = [
    path('sto/', get_sto),
    path('create-sto/', put_sto),
]