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

from configurator.models import DeviceSetting
from configurator.serializers import DeviceSettingSerializer
from logger.serializers import LogSerializer
from logger.models import Log   
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
# Create your views here.
@csrf_exempt
def device_settings_list(request, dpk):
    """
    List all logs, or create a new log.
    """
    if request.method == 'GET':
        settings = DeviceSetting.objects.filter(device_id=dpk)
        serializer = DeviceSettingSerializer(settings, many=True)
        return JSONResponse(serializer.data)

    
def configure(request):
    c = {}
    c["request"] = request
    context = RequestContext(request)
    return render_to_response("configurator/index.html", c, context_instance=RequestContext(request))

def sample(request):
    c = {}
    c["request"] = request
    context = RequestContext(request)
    return render_to_response("configurator/sample.html", c, context_instance=RequestContext(request))

# ViewSets define the view behavior.
class DeviceSettingViewSet(viewsets.ModelViewSet):
    queryset = DeviceSetting.objects.all()
    serializer_class = DeviceSettingSerializer
    
    
# Temporary binding with server itself ( no need for rest-api for this)
# Settings to be read from user (Configurator input fields)
GENERAL_SETTINGS = {
    'Name Server': ('name-server', 'default-name-server', 'M'),
    'Pool Id': ('pool-id', 'default-pool-id', 'M'),
    'Subrcibe': ('subscribe-id', 'default-id', 'M')
}
# Format <Input Field Label> : (<UCSM_Mapping_Label>, <Default_Value>,
#                                       <Field_Req>, <Field_Type>)
# <UCSM_Mapping_Label> is must for identifying the text control inputting desired field
# <Default_Value> is the one which is displayed as place holder in html page
#               (Default value if no other value provided)
# <Field_Req>: can be any of (Mandator, Basic, Optional, Advanced)
# <Field_Type>: can be any of (ALPHA, NUMERIC, ALPHA_NUMERIC, PASSWORD,
#                               IP, MULTIPLE_IP, COMPOUND, EMAIL, CUSTOM)
FI_SETTINGS = {
    'FI IPADDRESS':['fi-ip-address', '8.8.8.8', 'M'],
    'FI Descrition':['fi-description', 'fi-default-desc', 'M'],
}
COBBLER_SETTINGS = {
    'Compute Hosts': ('compute-hosts', 'compute-default-nodes', 'M'),
    'Network Hosts': ('network-hosts', 'network-default-nodes', 'M'),
}
SWITCH_SETTINGS = {
    'Host Name': ('host-name', 'default-host-name', 'M'),
    'User Name': ('user-name', 'default-user-name', 'M'),
}

SETTINGS = {}
SETTINGS["GENERAL_SETTINGS"] = GENERAL_SETTINGS
SETTINGS["FI_SETTINGS"] = FI_SETTINGS
SETTINGS["COBBLER_SETTINGS"] = COBBLER_SETTINGS
SETTINGS["SWITCH_SETTINGS"] = SWITCH_SETTINGS

@csrf_exempt
def server_binding_sample(request):
    c = {}
    c["request"] = request
    c["SETTINGS"] = SETTINGS
    context = RequestContext(request)
    return render_to_response("configurator/server_binding_sample.html", c, context_instance=RequestContext(request))
    # return HttpResponse("Hello World... This is Sriram's First app")

@csrf_exempt
def server_binding_post(request):
    print "post came from server_binding"
    
