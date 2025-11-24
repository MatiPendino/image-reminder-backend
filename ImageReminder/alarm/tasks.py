from celery import shared_task
from datetime import datetime
from notification.models import FCMToken
from notification.utils import get_fcm_object
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
    """
        This task will filter the alarms in the current time and weekday and will send 
        a push notification
    """
    # Alarm filter by hour and minute
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    current_weekday = WEEKDAYS_MAP[now.weekday()]
    alarms = Alarm.objects.filter(
        time__hour=current_hour,
        time__minute=current_minute
    ).select_related('alarm_user')

    fcm = get_fcm_object()
    notification_title = 'Alarm Notification'

    for alarm in alarms:
        weekdays = alarm.weekdays
        # If the current weekday matches one of the alarm weekdays list, the push message is sent
        for day in weekdays:
            if day['full'] == current_weekday:
                alarm_user = alarm.alarm_user
                fcm_tokens = FCMToken.objects.filter(device_id=alarm_user.device_uuid)

                for fcm_token in fcm_tokens:
                    notification_body = f'Don’t forget to watch your {alarm.title} photo!'
                    data = {
                        "type": "alarm",         
                        "alarm_id": str(alarm.id),
                        "title": alarm.title,
                        "image": alarm.image.url if alarm.image else "",
                        "time": alarm.time.strftime("%H:%M"),
                        "route": "AlarmScreen"
                    }
                    fcm.notify(
                        fcm_token=fcm_token.token_id, 
                        notification_title=notification_title, 
                        notification_body=notification_body,
                        data_payload=data
                    )
