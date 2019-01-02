from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import logging
import os
from .models import Competition
from api.serializers import CompetitionSerializer
from rest_framework import generics


class CompetitionListCreate(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

# def index(request):
#     # logger = logging.getLogger(__name__)
#     # logger.debug('this is another log')
#
#     # required to start server with: docker-compose run --service-ports web
#     # import pdb; pdb.set_trace()
#
#     competions = Competition.objects.all()
#
#     template = loader.get_template('api/competition.html')
#     context = {
#         'competitions': competitions
#     }
#
#     return HttpResponse(template.render(context, request))

# def competition(request, competition_id):
#     competition = Competition.objects.filter(pk=competition_id).first()

# return JsonResponse(competition.to_json())

# def competitions(request):
# return JsonResponse({'competitions': [c.to_json() for c in Competition.objects.all()]})

# homepage/register
# dashboard/auth fitbit
# get users competitions
# subscribe to competition
# get user info
