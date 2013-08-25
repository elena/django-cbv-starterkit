# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.db import models
from model_utils.managers import PassThroughManager
from tagging.fields import TagField
from contrib.abstract.basics.models import AbstractBasic
from contrib.abstract.contents import querysets
from contrib.abstract.contents import utils


class Content(AbstractBasic):

    title = models.CharField(max_length=200)
    headline = models.CharField(max_length=200, blank=True, default='')
    content = models.TextField(blank=True, default='')
    featured_content = models.TextField(blank=True, default='')

    is_indexable = models.BooleanField('indexable', db_index=True, default=True,
        help_text='Should this page be indexed by search engines?')

    meta_description = models.CharField(max_length=200, blank=True, default='',
        help_text='Optional short description for use by search engines.')

    tags = TagField(blank=True, default='',
        help_text='Separate tags with spaces, put quotes around multiple-word '
                  'tags.')

    template = models.CharField(max_length=100, blank=True, default='',
                                help_text='Example: "app/model_detail.html".')

    objects = PassThroughManager().for_queryset_class(
        querysets.ContentQuerySet)()

    class Meta(AbstractBasic.Meta):
        abstract = True
        ordering = ('title',)

    def __str__(self):
        return self.title

    @property
    def heading(self):
        return self.headline if self.headline else self.title


class ContentWithSite(Content):

    site = models.ForeignKey('sites.Site', default=Site.objects.get_current)

    objects = PassThroughManager().for_queryset_class(
        querysets.SiteContentQuerySet)()

    class Meta(Content.Meta):
        abstract = True


class ContentWithSlug(ContentWithSite):

    slug = models.SlugField()

    class Meta(ContentWithSite.Meta):
        abstract = True
        unique_together = ('site', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            queryset = self.__class__.objects.filter(site=self.site)
            self.slug = utils.generate_unique_slug(self.title, queryset)
        return super(ContentWithSlug, self).save(*args, **kwargs)
