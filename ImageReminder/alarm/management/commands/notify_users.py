from django.core.management.base import BaseCommand
from fcm_django.models import FCMDevice
from firebase_admin import credentials
import firebase_admin
from exponent_server_sdk import PushClient, PushMessage, PushServerError
from exponent_server_sdk import DeviceNotRegisteredError, InvalidCredentialsError
from alarm.models import AlarmUser, Alarm


# Ensure Firebase is initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('alarm/photo-reminder.json')
    print(cred)
    firebase_admin.initialize_app(cred)


class Command(BaseCommand):
    def handle(self, *args, **options):
        devices = FCMDevice.objects.all()
        expo_push_client = PushClient()
        title = "PhotoReminder"

        try:
            messages = []
            for device in devices:
                token = device.registration_id
                if not token.startswith('ExponentPushToken'):
                    print(f'Invalid token: {token}')
                    continue

                alarm_user = AlarmUser.objects.filter(device_uuid=device.name).first()
                if alarm_user:
                    alarms = Alarm.objects.filter(alarm_user=alarm_user)
                    for alarm in alarms:
                        body = f'Don´t forget to watch your {alarm.title} photo!'
                        messages.append(
                            PushMessage(
                                to=token,
                                title=title,
                                body=body,
                            )
                        )
                    
            # Send messages
            response = expo_push_client.publish_multiple(messages)
            print("push notifications sent successfully!")
        except (PushServerError, DeviceNotRegisteredError, InvalidCredentialsError) as exc:
            print("There was an error sending the push notifications")