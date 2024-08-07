from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'', AlarmViewset)

urlpatterns = [
    path('register_device/', RegisterDevice.as_view()),
    path('sent_nots/', NotifyUsers.as_view()),
    path('', include(router.urls)),
]
