from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from fcm_django.models import FCMDevice
from sentry_sdk import capture_message, set_context
from .models import Alarm
from .serializers import AlarmSerializer

class AlarmViewset(viewsets.ModelViewSet):
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
            set_context("Request Details", {
                "request_data": request.data,
                "error": "Token is required"
            })
            capture_message("Token is missing in RegisterDevice API", level="error")
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.alarm_user:
            set_context("Request Details", {
                "request_data": request.data,
                "alarm_user": str(request.alarm_user),
                "error": "Alarm user not found"
            })
            capture_message("Alarm user not found in RegisterDevice API", level="error")
            return Response({"error": "Alarm user not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        device, created = FCMDevice.objects.get_or_create(
            registration_id=token,
            defaults={
                'name': request.alarm_user.device_uuid,
                'device_id': str(request.alarm_user.device_uuid),
                'type': 'android'
            }
        )
        if not created:
            device.registration_id = token
            device.save()
            return Response({"message": "Device already registered"}, status=status.HTTP_200_OK)
        
        return Response({"message": "Device registered successfully"}, status=status.HTTP_201_CREATED)
