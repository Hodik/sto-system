from django.urls import path, include
from website.views import *
urlpatterns = [
    path('stos/', StoList.as_view()),
    path('stos/<int:pk>', StoDetail.as_view()),
    path('review/', ReviewList.as_view()),
]