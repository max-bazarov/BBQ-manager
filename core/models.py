from django.db import models


class ArchiveMixin(models.Model):
    archived = models.BooleanField(
        'is archived',
        default=False
    )

