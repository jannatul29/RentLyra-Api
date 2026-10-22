import os
import urllib.request

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.files import File
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from users import storage_backends


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    
    class GenderType(models.TextChoices):
        NOT_SPECIFIED = '', _('Prefer not to say')
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')
        CISGENDER = 'cisgender', _('Cisgender')
        TRANSGENDER = 'transgender', _('Transgender')

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    phone = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Example: +16045551234")
    profile_image = models.ImageField(max_length=255, blank=True, storage=storage_backends.ProfileImageMediaStorage, help_text="Image Field")
    source_url = models.URLField(max_length=1000, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True, choices=GenderType.choices, help_text="Example: Female")
    country = models.CharField(max_length=255, blank=True, help_text="Example: Canada")
    country_code = models.CharField(max_length=3, blank=True, help_text="Example: CA")
    state = models.CharField(max_length=255, blank=True, help_text="Example: Vancouver")
    city = models.CharField(max_length=255, blank=True, help_text="Toronto")
    address = models.CharField(max_length=255, blank=True, help_text="Example: 101-11 West Avenue, Vancouver BC V6H 1L9Vancouver BC V6H 1L9")
    verification_code = models.IntegerField(blank=True, null=True, help_text="Integer Field")
    is_real_email = models.BooleanField(default=True, help_text="Boolean Field")
    alternative_email = models.EmailField(unique=True, null=True, blank=True, help_text="Example: example@gmail.com")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self.source_url and not self.profile_image:
            result = urllib.request.urlretrieve(str(self.source_url))
            with open(result[0], "rb") as downloaded_file:
                self.profile_image.save(os.path.basename(self.source_url), File(downloaded_file), save=False)

        super(User, self).save(*args, **kwargs)


class PhoneEmailVerification(models.Model):
    class Meta:
        unique_together = (('phone_email', 'activation_code'),)
        verbose_name = 'OTP Confirmation'
        verbose_name_plural = 'OTP Confirmation'

    class VerificationType(models.TextChoices):
        Email = 'email', _('Email')
        Phone_Number = 'phone_number', _('Phone Number')

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User ID")
    phone_email = models.CharField(max_length=50, help_text="Example: example@gmail.com or +16045551234")
    activation_code = models.IntegerField(help_text="Integer Field (4 digits)")
    verification_type = models.CharField(max_length=50, choices=VerificationType.choices, help_text="Choice Field")

    def __str__(self):
        return self.phone_email
