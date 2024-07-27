from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Alarm, AlarmUser

class AlarmUserResources(resources.ModelResource):
    class Meta:
        model = AlarmUser

class AlarmUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('device_uuid',)
    list_display = ('device_uuid',)
    resource_class = AlarmUser


class AlarmResources(resources.ModelResource):
    class Meta:
        model = Alarm

class AlarmAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('title', 'alarm_user__device_uuid')
    list_display = ('title', 'get_device_uuid')

    def get_device_uuid(self, obj):
        return obj.alarm_user.device_uuid
    get_device_uuid.admin_order_field = 'alarm_user__device_uuid'
    get_device_uuid.short_description = 'Device UUID'


admin.site.register(AlarmUser, AlarmUserAdmin)
admin.site.register(Alarm, AlarmAdmin)