from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'alarm', AlarmViewset)

urlpatterns = [
    path('register_device/', RegisterDevice.as_view(), name='register_device'),
    path('', include(router.urls)),
]
