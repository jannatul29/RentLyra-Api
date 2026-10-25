import random
from datetime import datetime, timedelta

import phonenumbers
import pycountry
import pytz
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.db import transaction, IntegrityError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
from validate_email import validate_email

from users.models import User, PhoneEmailVerification

utc = pytz.UTC


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text="Example: example@gmail.com"
    )

    password = serializers.CharField(write_only=True, required=True, help_text="Not less than 8 characters")
    password2 = serializers.CharField(write_only=True, required=False, help_text="Same as password")
    first_name = serializers.CharField(required=True, help_text="Example: John")
    last_name = serializers.CharField(required=True, help_text="Example: Doe")

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords are not identical."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'].lower(),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False
        )

        user.set_password(validated_data['password'])
        user.save()

        group, created = Group.objects.get_or_create(name='Renter')
        group.user_set.add(user)

        return user