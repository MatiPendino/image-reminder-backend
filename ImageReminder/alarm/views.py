from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
# from fcm_django.models import FCMDevice
from sentry_sdk import capture_message, set_context
from notification.models import FCMToken
from .models import Alarm
from .serializers import AlarmSerializer

class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer

    def get_queryset(self):
        return Alarm.objects.filter(alarm_user=self.request.alarm_user).order_by('time')

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            data['alarm_user'] = request.alarm_user.id 

            # Pass the modified data to the serializer
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            capture_message(str(e), level="error")
            return Response({'error': 'Error processing the request'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            data = request.data
            data['alarm_user'] = request.alarm_user.id

            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)
        except Exception as e:
            capture_message(str(e), level="error")
            return Response({'error': 'Error processing the request'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterDevice(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            raise ValueError('Token is required')

        if not request.alarm_user:
            raise ValueError('Alarm user is required')
        
        device, created = FCMToken.objects.get_or_create(
            token_id=token,
            defaults={
                'device_id': str(request.alarm_user.device_uuid),
                'type': FCMToken.ANDROID
            }
        )
        if not created:
            device.registration_id = token
            device.save()
            return Response({"message": "Device already registered"}, status=status.HTTP_200_OK)
        
        return Response({"message": "Device registered successfully"}, status=status.HTTP_201_CREATED)
