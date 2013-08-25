# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class LiveQuerySet(models.query.QuerySet):

    def active(self):
        now = timezone.now()
        return self.filter(is_enabled=True).filter(
            models.Q(time_publish__lte=now),
            models.Q(time_expire__isnull=True) | models.Q(time_expire__gte=now))

    def featured(self):
        return self.filter(is_featured=True)
