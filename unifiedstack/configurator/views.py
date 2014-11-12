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

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
# Create your views here.

def configure(request):
    c = {}
    c["request"] = request
    context = RequestContext(request)
    return render_to_response("logger/index.html", c, context_instance=RequestContext(request))

def sample(request):
    c = {}
    c["request"] = request
    context = RequestContext(request)
    return render_to_response("logger/sample.html", c, context_instance=RequestContext(request))