from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from logger.models import Log, Device, ConsoleLog
from logger.serializers import LogSerializer, DeviceSerializer, ConsoleLogSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
# Create your views here.

def sample(request):
    c = {}
    c["request"] = request
    context = RequestContext(request)
    return render_to_response("logger/sample.html", c, context_instance=RequestContext(request))


@csrf_exempt
def log_list(request):
    """
    List all logs, or create a new log.
    """
    if request.method == 'GET':
        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        serializer = LogSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def log_detail(request, pk):
    """
    Retrieve, update or delete a log.
    """
    try:
        log = Log.objects.get(pk=pk)
    except Log.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LogSerializer(log)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LogSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def device_list(request):
    """
    List all logs, or create a new log.
    """
    if request.method == 'GET':
        logs = Device.objects.all()
        serializer = DeviceSerializer(logs, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        print "came till post"
        print "check this",request.body, ".thats all"
        data = JSONParser().parse(request)
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def device_detail(request, pk):
    """
    Retrieve, update or delete a log.
    """
    try:
        device = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeviceSerializer(device)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DeviceSerializer(device, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def list_n_console_logs(request):
    console_logs = ConsoleLog.objects.all()
    serializer = ConsoleLogSerializer(console_logs, many=True)
    return JSONResponse(serializer.data)
    
# ViewSets define the view behavior.
class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    
class ConsoleLogViewSet(viewsets.ModelViewSet):
    queryset = ConsoleLog.objects.all()
    serializer_class = ConsoleLogSerializer
    
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    
