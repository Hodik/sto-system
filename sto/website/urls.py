from django.urls import path, include
from website.views import *

urlpatterns = [
    path('start/', start_view),
]