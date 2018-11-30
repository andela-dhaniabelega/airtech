from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import parsers, status
from django.contrib.auth import get_user_model

from core.api.serializers import UserCreateSerializer, UserLoginSerializer, PhotoUploadSerializer
from core.utils import get_single_object
from airtech.settings import DEFAULT_IMAGE

User = get_user_model()


class UserCreate(APIView):
    """
    Creates a new user
    :param
    :return
    """
    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    Implements User Login
    """
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoUpdateDestroy(APIView):
    """
    Handles Photo Upload (and Update) and Deletion
    """
    def put(self, request, user_id, format=None):
        parser_classes = (parsers.MultiPartParser, parsers.FormParser)
        user = get_single_object(user_id, User)
        serializer = PhotoUploadSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        user = get_single_object(user_id, User)
        setattr(user, 'photo', DEFAULT_IMAGE)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
