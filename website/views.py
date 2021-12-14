from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from website.models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from website.serializers import *

from django.http import HttpResponseNotAllowed
from django.utils.log import log_response
from functools import wraps

def require_http_methods(request_method_list):
    """
    Decorator to make a view only accept particular request methods.  Usage::

        @require_http_methods(["GET", "POST"])
        def my_view(request):
            # I can assume now that only GET or POST requests make it this far
            # ...

    Note that request methods should be in uppercase.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method not in request_method_list:
                response = HttpResponseNotAllowed(request_method_list)
                log_response(
                    'Method Not Allowed (%s): %s', request.method, request.path,
                    response=response,
                    request=request,
                )
                return response
            return func(request, *args, **kwargs)
        return inner
    return decorator


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
