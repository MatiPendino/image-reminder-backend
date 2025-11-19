import uuid
import os
import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from alarm.models import Alarm, AlarmUser

class AlarmViewSetTests(APITestCase):
    def setUp(self):
        self.alarm_user = AlarmUser.objects.create(device_uuid=uuid.uuid4())
        self.client = APIClient()

    def test_create_alarm(self):
        image_path = finders.find('img/sydney_night.jpg')
        device_uuid = self.alarm_user.device_uuid
        self.client.defaults['HTTP_DEVICE_ID'] = str(device_uuid)

        # Use SimpleUploadedFile to simulate an image file upload
        with open(image_path, 'rb') as image_file:
            image = SimpleUploadedFile(
                'sydney_night.jpg', 
                image_file.read(), 
                content_type='image/jpeg'
            )
        
            data = {
                'title': 'Morning Alarm',
                'time': '07:30',
                'alarm_user': self.alarm_user,
                'weekdays': json.dumps([
                    {
                        "abbreviation": "T",
                        "full": "Tuesday"
                    },
                    {
                        "abbreviation": "T",
                        "full": "Thursday"
                    },
                ]),
                'image': image
            }
            response = self.client.post(
                reverse('alarm-list'), data, format='multipart', HTTP_DEVICE_ID=device_uuid
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Alarm.objects.count(), 1)
            self.assertEqual(Alarm.objects.all().first().title, 'Morning Alarm')

    def test_update_alarm(self):
        image_path = os.path.join(settings.MEDIA_ROOT, 'alarm', 'sydney_night.jpg')
        device_uuid = self.alarm_user.device_uuid
        self.client.defaults['HTTP_DEVICE_ID'] = str(device_uuid)
    
        alarm = Alarm.objects.create(
            title='Morning Alarm', 
            time='08:00', 
            alarm_user=self.alarm_user,
            weekdays=json.dumps([
                {
                    "abbreviation": "T",
                    "full": "Tuesday"
                },
                {
                    "abbreviation": "T",
                    "full": "Thursday"
                },
            ]),
            image=image_path
        )
        data = {
            'title': 'Updated Alarm',
            'weekdays': alarm.weekdays,
            'image': alarm.image,
            'time': alarm.time
        }
        response = self.client.put(
            reverse('alarm-detail', kwargs={'pk': alarm.id}), 
            data, 
            format='multipart',
            HTTP_DEVICE_ID=device_uuid
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Alarm.objects.get(id=alarm.id).title, 'Updated Alarm')

    def test_delete_alarm(self):
        image_path = os.path.join(settings.MEDIA_ROOT, 'alarm', 'sydney_night.jpg')
        device_uuid = self.alarm_user.device_uuid
        self.client.defaults['HTTP_DEVICE_ID'] = str(device_uuid)

        alarm = Alarm.objects.create(
            title='Morning Alarm', 
            time='09:30', 
            alarm_user=self.alarm_user,
            weekdays=json.dumps([
                {
                    "abbreviation": "T",
                    "full": "Tuesday"
                },
                {
                    "abbreviation": "T",
                    "full": "Thursday"
                },
            ]),
            image=image_path
        )
        delete_url = reverse('alarm-detail', kwargs={'pk': alarm.id})
        response = self.client.delete(delete_url, HTTP_DEVICE_ID=device_uuid)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Alarm.objects.count(), 0)
