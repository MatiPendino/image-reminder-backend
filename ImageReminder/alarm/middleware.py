from .models import AlarmUser

class DeviceIdentifierMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        device_uuid = request.headers.get('Device-ID')
        if device_uuid:
            alarm_user, created = AlarmUser.objects.get_or_create(device_uuid=device_uuid)
            request.alarm_user = alarm_user

        response = self.get_response(request)
        return response