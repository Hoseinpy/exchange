from django.contrib import admin
from .models import AsUserLevel1CheckModel, AsUserLevel2CheckModel


@admin.register(AsUserLevel1CheckModel)
class AsUserLevel1CheckModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'father_name', 'national_code', 'phone_number', 'uuid', 'created_at']


@admin.register(AsUserLevel2CheckModel)
class AsUserLevel2CheckModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'authentication_image', 'uuid', 'created_at']