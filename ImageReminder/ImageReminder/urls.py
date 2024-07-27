from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from django.urls import path, re_path, include
from alarm import urls as alarm_urls

admin.site.site_header = 'ImageReminder Admin'
admin.site.site_title = 'ImageReminder Admin Portal'
admin.site.index_title = 'Welcome to the ImageReminder Portal'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alarms/', include(alarm_urls))
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]
