from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from notification.models import FCMToken
from .serializers import FCMTokenSerializer


class FCMTokenAPIView(APIView):
    def post(self, request):
        """
            Create or retrieve FCMToken
            Return FCMToken serialized object
        """
        token = request.data.get('fcm_token')
        device_id = request.data.get('device_id')
        print(device_id)

        with transaction.atomic():
            fcm_token, was_created = FCMToken.objects.get_or_create(
                token_id=token,
                device_id=device_id
            )

        fcm_serializer = FCMTokenSerializer(fcm_token)

        return Response(
            fcm_serializer.data, 
            status=status.HTTP_201_CREATED if was_created else status.HTTP_200_OK
        )
    
