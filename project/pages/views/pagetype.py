# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views import generic
from project.pages.forms import PageTypeForm
from project.pages.models import PageType


class QuerySetMixin(object): #LoginRequiredMixin):

    model = PageType

    def get_queryset(self, *args, **kwargs):
        queryset = super(QuerySetMixin, self).get_queryset(*args, **kwargs)
        return queryset


class ListView(QuerySetMixin, generic.ListView):

    required_permissions = ('pages.read_pagetype',)


class DetailView(QuerySetMixin, generic.DetailView):

    required_permissions = ('pages.read_pagetype',)


class EditMixin(QuerySetMixin):

    form_class = PageTypeForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(EditMixin, self).get_form_kwargs(*args, **kwargs)
        form_kwargs.update({'user': self.request.user})
        return form_kwargs

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Saved page type.')
        return reverse('pages:pagetype_list')


class CreateView(EditMixin, generic.CreateView):

    required_permissions = ('pages.add_page',)


class UpdateView(EditMixin, generic.UpdateView):

    required_permissions = ('pages.change_page',)


class DeleteView(QuerySetMixin, generic.DeleteView):

    required_permissions = ('pages.delete_page',)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Deleted page type.')
        return reverse('pages:pagetype_list')
