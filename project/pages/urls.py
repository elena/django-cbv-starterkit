# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from project.pages.views import pages, pagetype

urls = patterns('',

    url(r'^$',
        pages.ListView.as_view(), name='page_list'),
    url(r'^(?P<page>\d+)$',
        pages.ListView.as_view(), name='paginated_page_list'),
    url(r'^add$',
        pages.CreateView.as_view(), name='page_add'),
    url(r'^(?P<pk>\d+)/edit$',
        pages.UpdateView.as_view(), name='page_edit'),
    url(r'^(?P<pk>\d+)/delete$',
        pages.DeleteView.as_view(), name='page_delete'),


    # Page types
    url(r'^types/$',
        pagetype.ListView.as_view(), name='pagetype_list'),
    url(r'^types/(?P<pk>\d+)/$',
        pagetype.DetailView.as_view(), name='pagetype_detail'),
    url(r'^types/add$',
        pagetype.CreateView.as_view(), name='pagetype_add'),
    url(r'^types/(?P<pk>\d+)/edit$',
        pagetype.UpdateView.as_view(), name='pagetype_edit'),
    url(r'^types/(?P<pk>\d+)/delete$',
        pagetype.DeleteView.as_view(), name='pagetype_delete'),

)

urlpatterns = patterns('',

    (r'^', include(urls, namespace='pages')),

)
