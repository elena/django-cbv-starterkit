# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db.models import Max


def set_order(sender, instance, raw, **kwargs):
    """Determine and set the order value for a new model instance."""

    if not instance.order and not raw:
        order = instance.__class__.objects.aggregate(
            order=Max('order')).get('order')
        instance.order = order + 1 if order is not None else 1
