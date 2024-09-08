from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'alarm', AlarmViewset)

def sentry_error(request):
    division_zero = 1 / 0

urlpatterns = [
    path('register_device/', RegisterDevice.as_view(), name='register_device'),
    path('', include(router.urls)),
    path('sentry_error/', sentry_error),
]
