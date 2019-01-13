from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from api.models import Competition


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'


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
        fields = ( "id", "username", "password", )


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
