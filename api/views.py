from django.shortcuts import render
from django.http import HttpResponse
import logging

def index(request):
    logger = logging.getLogger(__name__)

    logger.debug('this is a log')
    
    # required to start server with: docker-compose run --service-ports web
    # import pdb; pdb.set_trace()

    print('oh fuck i could do this')

    return HttpResponse("Hello, world. You're at the polls index.<h1>hi</h1>" + request.GET.get('foo', 'default'))