from django.db import models
import uuid

class AlarmUser(models.Model):
    device_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return str(self.device_uuid)
    

class Alarm(models.Model):
    alarm_user = models.ForeignKey(AlarmUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='alarm/')
    time = models.TimeField()
    weekdays = models.JSONField()

    def __str__(self):
        return self.title