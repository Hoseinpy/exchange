from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    verify_code = models.CharField(max_length=72, null=True)
    ir_wallet = models.DecimalField(max_digits=30, decimal_places=0, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CurrencyWallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=30, decimal_places=2)

    def __str__(self):
        return self.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance=None, created=False, **kwargs):
    if created:
        CurrencyWallet.objects.create(name='btc', user=instance, price=0)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    about_me = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='user-profile-image/', blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)