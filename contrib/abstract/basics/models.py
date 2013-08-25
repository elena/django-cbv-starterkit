# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from model_utils.managers import PassThroughManager

from contrib.abstract.basics import settings
from contrib.abstract.basics.querysets import LiveQuerySet


class AbstractAuthor(models.Model):

    user_created = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    """User who first created this object (required)."""

    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    """User who last saved this object (required)."""

    class Meta(object):
        abstract = True

    def save(self, user=None, **kwargs):
        if user is not None:
            if not self.pk:
                self.user_created = user
            self.user_updated = user
        return super(AbstractAuthor, self).save(**kwargs)


class AbstractTime(models.Model):

    time_created = models.DateTimeField(auto_now_add=True, editable=False)
    """:py:class:`datetime` for when this object was first created."""

    time_updated = models.DateTimeField(auto_now=True, editable=False)
    """:py:class:`datetime` for when this object was last saved."""

    class Meta(object):
        abstract = True


class AbstractLive(models.Model):

    is_enabled = models.BooleanField('enabled', db_index=True, default=True)
    is_featured = models.BooleanField('featured', db_index=True, default=False)

    time_publish = models.DateTimeField(db_index=True, default=timezone.now)
    """:py:class:`datetime` for when this object was published."""

    user_publish = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True, blank=True)
    """User who last published this object (required)."""

    time_expire = models.DateTimeField(db_index=True, null=True, blank=True)
    """:py:class:`datetime` for when this object expires."""

    objects = PassThroughManager().for_queryset_class(LiveQuerySet)()

    class Meta(object):
        abstract = True
        get_latest_by = 'time_publish'

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()


class AbstractBasic(AbstractAuthor, AbstractTime, AbstractLive):

    class Meta(object):
        abstract = True
