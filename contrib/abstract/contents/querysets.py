# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from contrib.abstract.basics.querysets import LiveQuerySet


class ContentQuerySet(LiveQuerySet):

    def indexable(self):
        return self.filter(is_indexable=True).active()


class SiteContentQuerySet(ContentQuerySet):

    def current_site(self):
        site = Site.objects.get_current()
        return self.filter(site=site)
