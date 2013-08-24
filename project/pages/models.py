# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

class PageType(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, default='')

    class Meta(object):
        ordering = ('title',)

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField()

    page = models.TextField(blank=True, default='')
    """:py:class:`unicode` page. Default: ``''``."""

    order = models.PositiveIntegerField(default=0)
    """Order number :py:class:`int` (required). Default: ``0``."""


    class Meta:
        ordering = ('order', 'title')

    def __str__(self):
        return self.title

admin.site.register(Page)
