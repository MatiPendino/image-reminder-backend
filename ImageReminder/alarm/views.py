from sentry_sdk import capture_message
from rest_framework import viewsets
from .models import Alarm
from .serializers import AlarmSerializer

class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer

    def get_queryset(self):
        return Alarm.objects.filter(alarm_user=self.request.alarm_user).order_by('time')

    def perform_create(self, serializer):
        serializer.save(alarm_user=self.request.alarm_user)

    def perform_update(self, serializer):
        serializer.save(alarm_user=self.request.alarm_user)

    def handle_exception(self, exc):
        capture_message(f"AlarmViewSet Exception: {str(exc)}")
        return super().handle_exception(exc)