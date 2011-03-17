# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import logging

def entry(request):
    logging.info(request.GET)
    return HttpResponse(str(request.GET))
    
    
