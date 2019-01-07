from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Competition
from api.serializers import CompetitionSerializer, LoginSerializer
from rest_framework import generics, status
from django.contrib.auth import get_user_model, login, logout
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response
import os
from django.utils.http import urlsafe_base64_encode
import requests
from django.shortcuts import redirect


class CompetitionListCreate(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


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


# TODO extract auth logic into another service

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def fitbit_store_auth(request):
    client_id = os.environ['FITBIT_CLIENT_ID']
    code = request.GET.get('code')

    data = {
        'client_id': client_id,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': f"http://{request.get_host()}/api/store_fitbit_auth",
        # 'expires_in': 2592000
        'expires_in': 30
    }
    r = _send_auth_request(request, data)

    if r.get('success'):
        return redirect('/')
    else:
        return redirect('/?errors=' + str(r.get('errors', '')))


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def fitbit_data(request):
    token_expiration = request.user.profile.token_expiration
    access_token = request.user.profile.access_token
    authorized = bool(access_token)
    expired = token_expiration and token_expiration < timezone.now()
    errors = None

    if expired:
        r = _refresh_token(request)
        authorized = r.get('success')
        errors = r.get('errors', None)

    data = {"authorized": authorized}

    if authorized:
        headers = {'Authorization': f"Bearer {access_token}"}
        response = requests.get('https://api.fitbit.com/1/user/-/activities/date/today.json', headers=headers).json()
        data['data'] = response

        if response.get('errors', None):
            errors = response.get('errors')
    else:
        data['auth_url']: _auth_url(request)

    if errors:
        data['errors'] = errors
        data['auth_url'] = _auth_url(request)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data)


def _auth_url(request):
    client_id = os.environ['FITBIT_CLIENT_ID']
    return f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri=" \
        f"http://{request.get_host()}/api/store_fitbit_auth&scope=activity%20heartrate%20profile%20social"


def _refresh_token(request):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': request.user.profile.refresh_token
    }

    return _send_auth_request(request, data)


def _send_auth_request(request, data):
    client_id = os.environ['FITBIT_CLIENT_ID']
    encoded_auth_key = urlsafe_base64_encode(str.encode(f"{client_id}:{os.environ['FITBIT_CLIENT_SECRET']}")).decode(
        "utf-8")
    headers = {
        'Authorization': f"Basic {encoded_auth_key}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data).json()
    access_token = response.get('access_token', None)
    refresh_token = response.get('refresh_token', None)
    user = request.user

    r = {'success': bool(access_token)}
    if response.get('errors', None):
        r['errors'] = str(response.get('errors'))
        return r

    if user and user.profile:
        user.profile.access_token = access_token
        user.profile.refresh_token = refresh_token
        user.profile.token_expiration = timezone.now() + timezone.timedelta(seconds=response.get('expires_in'))
        user.profile.save()

    return r
