import traceback
import os

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.custom_errors import ApiError, ApiAuthError
from .models import CompetitionInvitation, Competition
from api.serializers import LoginSerializer, CompetitionInvitationSerializer, CompetitionInvitationListSerializer, \
    CompetitionSerializer
from rest_framework import generics, status
from django.contrib.auth import get_user_model, login, logout
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import redirect
from api.services.auth_provider import AuthProvider
from api.services.fitbit_api_gateway import FitbitApiGateway
from api.services.competition_provider import CompetitionProvider


class CompetitionCreate(generics.CreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class CompetitionInvitationUpdate(generics.UpdateAPIView):
    queryset = CompetitionInvitation.objects.all()
    serializer_class = CompetitionInvitationSerializer

    def patch(self, request, *args, **kwargs):
        if request.data['accepted']:
            invitation = self.get_object()
            invitation.profile.competitions.add(invitation.competition)
            invitation.save()

        return self.partial_update(request, *args, **kwargs)


class CompetitionInvitationCreate(generics.ListCreateAPIView):
    serializer_class = CompetitionInvitationSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, *args, **kwargs):
        # Defaulting the sender to the current user
        request.data['sender'] = request.user.profile.id

        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.queryset = CompetitionInvitation.objects.filter(
            profile=request.user.profile, accepted__isnull=True)
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        return Response({
            'invitations': CompetitionInvitationListSerializer(self.queryset, many=True).data
        })


class CreateUser(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class LoginUser(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid()

        user = self.serializer.validated_data

        if user:
            login(request, user)

            return Response({
                "success": True,
                "user": UserSerializer(user, context=self.get_serializer_context()).data
            })
        else:
            return Response({
                "success": False,
                "message": 'Username and password not found'
            })


class LogoutUser(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        logout(request)

        return Response({"success": True})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def fitbit_store_auth(request):
    try:
        provider = AuthProvider(request.user.profile)
        provider.store_fitbit_auth(request.GET.get(
            'code'), _get_url_start(request), request.user.profile)
    except (ApiError, ApiAuthError):
        traceback.print_exc()
        return redirect('/#/?error=Error during fitbit auth')

    return redirect('/#')


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def simple_competitions_list(request):
    try:
        profile = request.user.profile
        provider = CompetitionProvider(profile)
        data = provider.simple_competitions(profile)
        return _successful_response(data)
    except ApiAuthError:
        return _api_auth_error_response(request)
    except ApiError as error:
        traceback.print_exc()
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
# TODO add perms for competition detail viewing
def competition_details(request, competition_id):
    try:
        profile = request.user.profile
        provider = CompetitionProvider(profile)
        data = provider.detailed_competition(profile, competition_id)
        return _successful_response(data)
    except ObjectDoesNotExist:
        return Response(f"Competition {competition_id} not found", status=status.HTTP_404_NOT_FOUND)
    except ApiAuthError:
        return _api_auth_error_response(request)
    except ApiError as error:
        traceback.print_exc()
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)


def _successful_response(data):
    return Response({'data': data, 'authorized': True})


def _get_url_start(request):
    protocol = 'https://' if os.environ.get(
        'PRODUCTION', False) == 'true' else 'http://'
    url_start = protocol + request.get_host()
    print(f"Using url start: {url_start}")

    return url_start


def _auth_url(request):
    return FitbitApiGateway.auth_url(_get_url_start(request))


def _api_auth_error_response(request):
    return Response({
        'authorized': False,
        'auth_url': _auth_url(request)
    })
