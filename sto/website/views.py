from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def start_view(_):
    return HttpResponse("ok", status=200)