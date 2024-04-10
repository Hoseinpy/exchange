from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CurrencyWallet, CartBankModel, Currency


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("id", "email", "phone_number", "user_level", "balance", "is_authentication", "is_staff", "is_active",)
    list_filter = ("is_authentication", "user_level", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "balance", "first_name", "last_name", "father_name", "phone_number", "national_code")}),
        ("Permissions", {"fields": ("authentication_image", "user_level", "verify_code", "is_authentication", "is_superuser", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active"
            )}
         ),
    )
    search_fields = ("email", 'first_name', 'last_name', 'phone_number', 'national_code', 'father_name')
    ordering = ("id",)


@admin.register(CurrencyWallet)
class CurrencyWalletAdmin(admin.ModelAdmin):
    list_display = ("user", "currency", "price", 'code',)
    list_filter = ("user",)


@admin.register(CartBankModel)
class CartBankAdmin(admin.ModelAdmin):
    list_display = ("user", "cart_number", "is_accepted", "uuid")
    list_filter = ("user", "is_accepted")


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
