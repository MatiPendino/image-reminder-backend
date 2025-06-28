from django.db import models

class FCMToken(models.Model):
    ANDROID = 0
    IOS = 1
    WEB = 2
    TOKEN_TYPE_CHOICES = (
        (ANDROID, 'Android'),
        (IOS, 'iOS'),
        (WEB, 'Web'),
    )
    token_id = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255, null=True, blank=True)
    token_type = models.IntegerField(choices=TOKEN_TYPE_CHOICES, default=0)

    def __str__(self):
        return self.token_id