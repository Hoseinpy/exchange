from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CurrencyWallet, Profile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("id", "email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "verify_code", "ir_wallet")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "price",)
    list_filter = ("user",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user",)
    list_filter = ("user",)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CurrencyWallet, CurrencyAdmin)
admin.site.register(CustomUser, CustomUserAdmin)