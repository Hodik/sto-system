from django.shortcuts import render
from django.http import JsonResponse
from website.models import *
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@require_http_methods(["GET"])
def get_sto(request):
    stos = list(Sto.objects.all())

    rv: list = []
    for el in stos:
        rv.append({"owner_id": el.user.id, "name": el.name})
    return JsonResponse(rv, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def put_sto(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        Sto.objects.create(name=name, user=User.objects.first())
        return JsonResponse({"success": True})
