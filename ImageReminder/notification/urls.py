from django.urls import path
from .views import FCMTokenAPIView

urlpatterns = [
    path('fcm_token/', FCMTokenAPIView.as_view(), name='fcm_token'),
]