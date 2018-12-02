from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from core.models import Flight, Ticket

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


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

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return {
                    'user': payload,
                    'token': token
                }
            else:
                msg = 'Incorrect username or password'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Username and Password are required'
            raise serializers.ValidationError(msg)


class PhotoUploadSerializer(serializers.ModelSerializer):
    """
    Serializer to handle photo upload
    """
    photo = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = User
        fields = ('photo',)


class FlightSerializer(serializers.ModelSerializer):
    """
    Serializer to handle all CRUD operations on Flights
    """
    class Meta:
        model = Flight
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer to handle all CRUD Operations on Tickets
    """
    class Meta:
        model = Ticket
        fields = ('flight_details', 'owner', 'ticket_status')
