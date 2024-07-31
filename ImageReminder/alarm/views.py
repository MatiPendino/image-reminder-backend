from rest_framework import viewsets, status
from rest_framework.response import Response
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
            print(str(e))
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
            print(str(e))
            return Response({'error': 'Error processing the request'}, status=status.HTTP_400_BAD_REQUEST)
