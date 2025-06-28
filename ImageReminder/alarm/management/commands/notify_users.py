import sentry_sdk
from django.core.management.base import BaseCommand
from notification.models import FCMToken
from alarm.models import AlarmUser, Alarm


class Command(BaseCommand):
    def handle(self, *args, **options):
        devices = FCMToken.objects.all()
        title = "PhotoReminder"

        try:
            for device in devices:

                alarm_user = AlarmUser.objects.filter(device_uuid=device.name).first()
                if alarm_user:
                    alarms = Alarm.objects.filter(alarm_user=alarm_user)
                    for alarm in alarms:
                        body = f'Don´t forget to watch your {alarm.title} photo!'
                        
        except Exception as exc:
            print("There was an error sending the push notifications")
            sentry_sdk.capture_message(f"{str(exc)}", level='error')