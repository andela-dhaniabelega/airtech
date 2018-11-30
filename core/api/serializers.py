from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from core.utils import ExtendedEncoder

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used to create a new user
    """
    def validate(self, attrs):
        instance = User(**attrs)
        instance.clean()
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password',)
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer used to validate an email and password
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = 'User account disabled'
                    raise serializers.ValidationError(msg)

                # TODO: Add Token Based Authentication in Output 6.3
                serialized_user = ExtendedEncoder().default(user)
                return {
                    'user': serialized_user
                }
            else:
                msg = 'Incorrect username or password'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Username and Password are required'
            raise serializers.ValidationError(msg)
