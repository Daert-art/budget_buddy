from django.db import models
from apps.core.models.base_models import TimeStampedModel
from django.conf import settings


class Tag(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name
