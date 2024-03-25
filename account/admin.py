from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CurrencyWallet, CartBankModel, IrWallet


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("id", "email", "user_level", "is_authentication", "is_staff", "is_active",)
    list_filter = ("is_authentication", "user_level", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "father_name", "phone_number", "national_code", "authentication_image", "user_level", "verify_code")}),
        ("Permissions", {"fields": ("is_authentication", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class CurrencyWalletAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "price",)
    list_filter = ("user",)


class IrWalletAdmin(admin.ModelAdmin):
    list_display = ("user", "price",)
    list_filter = ("user",)


class CartBankAdmin(admin.ModelAdmin):
    list_display = ("user", "cart_number")
    list_filter = ("user",)


admin.site.register(IrWallet, IrWalletAdmin)
admin.site.register(CartBankModel, CartBankAdmin)
admin.site.register(CurrencyWallet, CurrencyWalletAdmin)
admin.site.register(CustomUser, CustomUserAdmin)