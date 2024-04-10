from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
import uuid


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
    class LevelChoice(models.TextChoices):
        level0 = 'Level0'
        level1 = 'Level1'
        level2 = 'Level2'
        level3 = 'Level3'

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    father_name = models.CharField(max_length=30, null=True)
    national_code = models.CharField(max_length=10, null=True)
    verify_code = models.CharField(max_length=72, null=True)
    user_level = models.CharField(max_length=6, choices=LevelChoice.choices, null=True, default=0)
    phone_number = models.CharField(max_length=14, null=True)
    authentication_image = models.ImageField(upload_to='user_info/', null=True)
    balance = models.DecimalField(max_digits=30, decimal_places=0, default=0)
    total_buying_and_selling = models.DecimalField(max_digits=30, decimal_places=0, default=0)

    is_authentication = models.BooleanField(default=False, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class CurrencyWallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=30, decimal_places=2, null=True)
    code = models.CharField(max_length=16, null=True)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.currency} -- {self.user}'


class Currency(models.Model):
    name = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name


class CartBankModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_number = models.CharField(max_length=16)
    uuid = models.CharField(max_length=15, editable=False)

    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user.email} -- {self.cart_number}'


# when user singup create token for him
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# when user singup create currency wallet 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_currency_wallet(sender, instance=None, created=False, **kwargs):
    if created:
        c = Currency.objects.all()
        for i in c:
            CurrencyWallet.objects.create(user=instance, currency=i, price=0, code=str(uuid.uuid4())[:16])