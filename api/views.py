from django.shortcuts import render
from django.http import HttpResponse
import logging
import os

def index(request):
    logger = logging.getLogger(__name__)

    logger.debug('this is another log')
    
    # required to start server with: docker-compose run --service-ports web
    # import pdb; pdb.set_trace()

    return HttpResponse("wacawaca!aasdfasdfasdfasdf.<h1>hi</h1>" + request.GET.get('foo', 'default'))