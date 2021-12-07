from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from website.models import *
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from website.serializers import *
@require_http_methods(["GET"])
def get_sto(request):
    if request.GET.get("format"):
        serializable = StoSerializer(Sto.objects.all(), many=True).serialized
        return HttpResponse(ObjectSerializer().serialize(serializable, request.GET.get("format")))

@csrf_exempt
@require_http_methods(["POST"])
def put_sto(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        Sto.objects.create(name=name, user=User.objects.first())
        return JsonResponse({"success": True})
