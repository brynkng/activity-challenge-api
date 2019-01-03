from rest_framework.permissions import AllowAny

from .models import Competition
from api.serializers import CompetitionSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model, login, authenticate, logout
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response


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
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return Response({
                    "success": True,
                    "user": UserSerializer(user, context=self.get_serializer_context()).data
                })
            else:
                return Response({
                    "success": False,
                    "message": "User is inactive"
                })

        return Response({
            "success": False,
            "message": "Username and password not found"
        })

class LogoutUser(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        logout(request)

        return Response({"success": True})