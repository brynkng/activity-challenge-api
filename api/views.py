from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import logging
import os
from .models import Competition
from api.serializers import CompetitionSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .serializers import UserSerializer


class CompetitionListCreate(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

class CreateUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer



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

# homepage/register
# dashboard/auth fitbit
# get users competitions
# subscribe to competition
# get user info
