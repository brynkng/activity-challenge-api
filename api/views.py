import traceback

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.custom_errors import ApiError
from api.services.fitbit_api import retrieve_fitbit_data, store_fitbit_auth
from .models import CompetitionInvitation
from api.serializers import LoginSerializer, CompetitionInvitationSerializer, CompetitionInvitationListSerializer
from rest_framework import generics, status
from django.contrib.auth import get_user_model, login, logout
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import redirect


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
        self.queryset = CompetitionInvitation.objects.filter(profile=request.user.profile, accepted__isnull=True)
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
        store_fitbit_auth(request.GET.get('code'), request.get_host(), request.user.profile)
    except ApiError:
        traceback.print_exc()

    return redirect('/#')


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def fitbit_data(request):
    try:
        r = retrieve_fitbit_data(request.user.profile, request.get_host())
        return Response(r)
    except ApiError as error:
        traceback.print_exc()
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)

