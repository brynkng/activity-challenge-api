import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.services.fitbit_api import retrieve_fitbit_data, store_fitbit_auth, get_competition_friend_list
from .models import Competition
from api.serializers import CompetitionSerializer, LoginSerializer
from rest_framework import generics, status
from django.contrib.auth import get_user_model, login, logout
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response
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


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def fitbit_store_auth(request):
    r = store_fitbit_auth(request.GET.get('code'), request.get_host(), request.user.profile)

    if r.get('success'):
        return redirect('/')
    else:
        return redirect('/?errors=' + str(r.get('errors', '')))


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def fitbit_data(request):
    try:
        r = retrieve_fitbit_data(request.user.profile, request.get_host())
        return Response(r)
    except Exception as error:
        traceback.print_exc()
        return Response("Something went wrong, please contact the developer.", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def competition_friend_list(request, competition_id):
    try:
        r = get_competition_friend_list(request.user.profile, Competition.objects.filter(id=competition_id).first())
        return Response(r)
    except Exception as error:
        traceback.print_exc()
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)



