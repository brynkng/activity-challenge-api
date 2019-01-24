from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from api.models import Competition, CompetitionInvitation, Profile

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ("id", "username", "password",)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise exceptions.ValidationError("User and password not found")
        elif not user.is_active:
            raise exceptions.ValidationError("User is inactive")
        else:
            return user


class ShowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "username")


class ProfileSerializer(serializers.ModelSerializer):
    user = ShowUserSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'user')
        depth = 1


class CompetitionInvitationListSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer()
    profile = ProfileSerializer()

    class Meta:
        model = CompetitionInvitation
        fields = ('id', 'competition', 'sender', 'profile')
        depth = 1


class CompetitionInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionInvitation
        fields = '__all__'


class CompetitionSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get('start') > attrs.get('end'):
            raise exceptions.ValidationError("Competition end date cannot be before start date")

        return attrs

    class Meta:
        model = Competition
        fields = '__all__'
