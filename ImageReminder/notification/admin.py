from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import FCMToken


class FCMTokenResources(resources.ModelResource):
    class Meta:
        model = FCMToken

class FCMTokenAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('token_id', 'device_id')
    list_display = ('token_id', 'device_id')
    resource_class = FCMTokenResources

admin.site.register(FCMToken, FCMTokenAdmin)