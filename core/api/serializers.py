from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        instance = User(**attrs)
        instance.clean()
        return attrs

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password',)
        extra_kwargs = {'password': {'write_only': True}}
