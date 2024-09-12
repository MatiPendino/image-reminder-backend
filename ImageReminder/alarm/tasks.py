import sentry_sdk
from celery import shared_task
from datetime import datetime
from exponent_server_sdk import PushClient, PushMessage
from fcm_django.models import FCMDevice
from .models import Alarm

WEEKDAYS_MAP = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

@shared_task
def check_and_send_alarms():
    '''
        This task will filter the alarms in the current time and weekday and will send 
        a push notification
    '''
    # Alarm filter by hour and minute
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    current_weekday = WEEKDAYS_MAP[now.weekday()]
    alarms = Alarm.objects.filter(
        time__hour=current_hour,
        time__minute=current_minute
    )

    expo_push_client = PushClient()
    title = "PhotoReminder"

    messages = []
    for alarm in alarms:
        weekdays = alarm.weekdays
        # If the current weekday matches one of the alarm weekdays list, the push message is sent
        for day in weekdays:
            if day['full'] == current_weekday:
                alarm_user = alarm.alarm_user
                devices = FCMDevice.objects.filter(name=alarm_user.device_uuid)

                for device in devices:
                    token = device.registration_id
                    if not token.startswith('ExponentPushToken'):
                        sentry_sdk.capture_message(f'Invalid token: {token}')
                        continue

                    body = f'Don’t forget to watch your {alarm.title} photo!'
                    messages.append(
                        PushMessage(
                            to=token,
                            title=title,
                            body=body,
                            data={'alarm_id': alarm.id}
                        )
                    )

    # Send messages
    if messages:
        response = expo_push_client.publish_multiple(messages)
