from rest_framework import serializers
from .models import Alarm

class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ['id', 'title', 'time', 'weekdays', 'image']
        read_only_fields = ['alarm_user']