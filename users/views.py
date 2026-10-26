from datetime import datetime

import pytz
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from datetime import timezone
from rest_framework import serializers
from rest_framework import generics, status, parsers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from users import serializers
from users.models import User


class UserCreate(generics.CreateAPIView):
    """
    Create a new user.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "An activation link is sent to your email. Please follow the instructions to activate your "
                           "account.",
                "data": []
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivate(generics.CreateAPIView):
    """
    Activate user
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserActivateSerializers
    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserActivateSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            update_last_login(None, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Activation successful",
                "data": {
                    'refresh': str(refresh),
                    'refresh_token_expires': refresh['exp'],
                    'access': str(refresh.access_token),
                    'access_token_expires': refresh.access_token['exp'],
                    "user_details": serializers.UserProfileSerializer(user).data
                }
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.CreateAPIView):
    """
    User Login
    """
    serializer_class = serializers.LoginSerializers
    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            update_last_login(None, user)
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Success",
                "data": {
                    'refresh': str(refresh),
                    'refresh_token_expires': refresh['exp'],
                    'access': str(refresh.access_token),
                    'access_token_expires': refresh.access_token['exp'],
                    "user_details": serializers.UserProfileSerializer(user).data
                }
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

