from celery import shared_task
from django.utils import timezone
from datetime import datetime
from exponent_server_sdk import PushClient, PushMessage, PushServerError
from exponent_server_sdk import DeviceNotRegisteredError, InvalidCredentialsError
from fcm_django.models import FCMDevice
from .models import Alarm

@shared_task
def check_and_send_alarms():
    now = datetime.now().time()
    alarms = Alarm.objects.filter(time=now)

    expo_push_client = PushClient()
    title = "PhotoReminder"

    messages = []
    for alarm in alarms:
        alarm_user = alarm.alarm_user
        devices = FCMDevice.objects.filter(name=alarm_user.device_uuid)

        for device in devices:
            token = device.registration_id
            if not token.startswith('ExponentPushToken'):
                print(f'Invalid token: {token}')
                continue

            body = f'Don’t forget to watch your {alarm.title} photo!'
            messages.append(
                PushMessage(
                    to=token,
                    title=title,
                    body=body,
                )
            )

    # Send messages
    if messages:
        response = expo_push_client.publish_multiple(messages)
        for res in response:
            if res.get('status') == 'error':
                print(f'Error: {res.get("message")}')
        print("Push notifications sent successfully!")