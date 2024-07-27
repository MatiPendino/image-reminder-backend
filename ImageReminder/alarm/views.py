from rest_framework import viewsets
from .models import Alarm
from .serializers import AlarmSerializer

class AlarmViewset(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer

    def get_queryset(self):
        print("llego")
        print(self.request)
        print(self.request.alarm_user)
        return Alarm.objects.filter(alarm_user=self.request.alarm_user)
    

