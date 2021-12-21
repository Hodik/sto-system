from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from website.models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from website.serializers import *
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
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

@csrf_exempt
@require_http_methods(["GET"])
def get_sto(request):
    if request.GET.get("format"):
        serializable = StoSerializer(Sto.objects.all(), many=True).serialized
        return HttpResponse(ObjectSerializer().serialize(serializable, request.GET.get("format")))

class MonthYearIterator:
    
    def __init__(self):
        self._years = [2019, 2020, 2021, 2022]
        self._months = ['apr', 'jun', 'jul', 'aug']
        self._years_counter = 0
        self._months_counter = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        rv: str = [self._years[self._years_counter], self._months[self._months_counter]]
        if self._months_counter == len(self._months) - 1 and self._years_counter == len(self._years) - 1:
            raise StopIteration("stop")
        elif self._months_counter == len(self._months) - 1: 
            self._years_counter += 1
            self._months_counter = 0
        else:
            self._months_counter += 1
        return rv


@csrf_exempt
@require_http_methods(["GET"])
def get_month_year(request):
    rv = []
    iter = MonthYearIterator()
    while True:
        try: 
            rv.append(next(iter))
        except StopIteration:
            break
    return JsonResponse({"data": rv})


@csrf_exempt
@require_http_methods(["POST"])
def put_sto(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        Sto.objects.create(name=name, user=User.objects.first())
        return JsonResponse({"success": True})


class StoList(generics.ListCreateAPIView):
    queryset = Sto.objects.all()
    serializer_class = StoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().all()
        
        queryset = list(filter(lambda x: x._STATE.search(), queryset))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sto.objects.all()
    serializer_class = StoSerializer
    def _check(self, request):
        instance = self.get_object()
        if ['status'] == list(request.data.keys()):
            if not instance._STATE.toggle(get_STATE_by_name(request.data['status'])()):
                raise Exception("Cannot toggle status")
        else:
            if 'status' in request.data.keys():
                raise Exception("Cannot edit status with other data")
            if not instance._STATE.edit():
                raise Exception("Sto not editable")
        
    def patch(self, request, *args, **kwargs):
        try:
            self._check(request)
        except Exception as e:
            return Response({"detail": e.__str__()}, status=status.HTTP_403_FORBIDDEN)
        return super().patch(request, *args, **kwargs)

class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = Review

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = Review